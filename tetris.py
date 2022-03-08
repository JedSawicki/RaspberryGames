#!/usr/bin/env python

# 90 DEGREES VERSION

import curses
import os
import random
import sys
import traceback

import signal

import threading
import time

from MAX7219 import MAX7219
from oled import I2C
from pyPS4Controller.controller import Controller


class Tetris:
    """
    A class to represent Tetris game.
    """

    def __init__(self, x, y):
        """init method"""
        self.points = 0
        self.i2c = I2C()
        self.game_over = False
        self.game_speed = 0.12
        self.led_matrix = []
        self.redraw = True
        self.board = []
        self.rows = x
        self.cols = y
        self.new_board()
        self.to_x = 32
        self.new_stone = []
        self.stone_x = 0
        self.stone_y = 0
        self.stone_to_draw = ""
        self.pause = False

        self.tetris_shapes = {
            'T': [[1, 1, 1],
                  [0, 1, 0]],

            'S': [[0, 1, 1],
                  [1, 1, 0]],

            'Z': [[1, 1, 0],
                  [0, 1, 1]],

            'J': [[1, 0, 0],
                  [1, 1, 1]],

            'L': [[0, 0, 1],
                  [1, 1, 1]],

            'I': [[1, 1, 1, 1]],

            'O': [[1, 1],
                  [1, 1]]
        }

    def new_block(self):
        """
        Method to generate new block.
        First it's generating random shape, then random rotation.
        New block Y is always 0 and X value oscillates in the middle of the board's width.
        """
        # print("new block!")
        next_shape = list(self.tetris_shapes.values())
        next_shape = random.choice(next_shape)
        self.new_stone = next_shape
        # generating random rotation of a block
        for _ in range(random.randrange(4)):
            self.new_stone = self.rotate_clockwise(self.new_stone)
            self.stone_to_draw = self.new_stone

        self.stone_x = int(self.cols / 2 - len(self.new_stone[0]) / 2)
        self.stone_y = 0
        if self.check_collision(self.board, self.new_stone, (self.stone_x, self.stone_y)):
            # if new block is out of map end the game
            self.game_over = True
            self.game_speed = 0.03
            self.i2c.game_over(self.points)
            time.sleep(1)
            sys.exit(0)

        return self.new_stone, self.stone_x, self.stone_y

    def new_board(self):
        """Method to generate new board, last row is filled with one's to simulate board border"""
        # print("new board!")
        self.board = [[0 for x in range(self.cols)]
                      for y in range(self.rows)]
        self.board += [[1 for x in range(self.cols)]]
        return self.board

    def remove_row(self, board, row):
        """Method to remove row from the list by python built-in function"""
        del board[row]
        self.points += 100
        self.i2c.draw_points(self.points)
        return [[0 for i in range(self.cols)]] + board

    def drop(self):
        """Method to change Y value of the stone already drawn on the map"""
        if not self.check_collision(self.board,
                                    self.new_stone,
                                    (self.stone_x, self.stone_y)):
            self.stone_y += 1

        while True:
            # for the whole game check if one of the rows is fulled, if so remove it from the list
            for i, row in enumerate(self.board[:-1]):
                # starting from the end
                if 0 not in row:
                    self.board = self.remove_row(self.board, i)
                    # self.score += 100
                    # self.message = self.next_shape + ' ' * (7 - len(str(self.score))) + str(self.score)
                    break
            else:
                break

    def move(self, delta_x):
        """Method to move block in horizontal position"""
        new_x = self.stone_x + delta_x
        if new_x < 0:
            new_x = 0
        if new_x > self.cols - len(self.new_stone[0]):
            new_x = self.cols - len(self.new_stone[0])
        if not self.check_collision(self.board,
                                    self.new_stone,
                                    (new_x, self.stone_y)):
            self.stone_x = new_x

    def rotate_clockwise(self, shape):
        """Method to rotate a block"""
        rotated_block = [[shape[y][x]
                          for y in range(len(shape))]
                         for x in range(len(shape[0]) - 1, -1, -1)]
        return rotated_block

    def check_collision(self, board, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    def rotate_stone(self):
        """Method to rotate clockwise current block, if collision occurred it's generating new block"""
        if not self.game_over:
            new_stone = self.rotate_clockwise(self.new_stone)
            if not self.check_collision(self.board,
                                        new_stone,
                                        (self.stone_x, self.stone_y)):
                self.new_stone = new_stone


class Utilities():
    """Business logic class"""

    def __init__(self, gameObject):
        self.gameObject = gameObject

    def join_matrixes(self, mat1, mat2, mat2_off):
        """
        Function to connect two matrix's.
        Example use: mat1 = game board, mat2 = new stone, mat2_offset = (new stone_x, new stone_y)
        Returns new connected matrix.
        """
        try:
            off_x, off_y = mat2_off
            for cy, row in enumerate(mat2):
                for cx, val in enumerate(row):
                    mat1[cy + off_y - 1][cx + off_x] += val
            return mat1
        except IndexError:
            pass

    def game_loop(self, device):
        self.gameObject.new_block()

        while not self.gameObject.check_collision(self.gameObject.board,
                                                  self.gameObject.new_stone,
                                                  (self.gameObject.stone_x,
                                                   self.gameObject.stone_y)):
            device.full_map(self.gameObject.new_stone,
                            self.gameObject.board,
                            (self.gameObject.stone_y,
                             self.gameObject.stone_x))

            while self.gameObject.pause and not self.gameObject.game_over:
                time.sleep(1)
            else:
                time.sleep(self.gameObject.game_speed)
            if self.gameObject.points >= 500:
                self.gameObject.game_speed = 0.1
            if self.gameObject.points >= 1000:
                self.gameObject.game_speed = 0.08
            self.gameObject.drop()
        else:
            try:
                self.gameObject.board = self.join_matrixes(self.gameObject.board,
                                                           self.gameObject.new_stone,
                                                           (self.gameObject.stone_x,
                                                            self.gameObject.stone_y))
            except IndexError:
                self.gameObject.i2c.keep_display = False
                self.gameObject.game_over = True
                self.gameObject.game_speed = 0.03


class MyController(Controller):

    def __init__(self, **kwargs):
        if 'gameObject' in kwargs:
            self.gameObject = kwargs.get('gameObject')
            kwargs.pop('gameObject')
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        self.gameObject.drop()

    def on_triangle_press(self):
        self.gameObject.rotate_stone()

    def on_right_arrow_press(self):
        self.gameObject.move(-1)

    def on_left_arrow_press(self):
        self.gameObject.move(1)

    def on_circle_press(self):
        self.gameObject.game_over = True
        self.gameObject.game_speed = 0.03
        self.gameObject.i2c.game_over(self.gameObject.points)

    def on_options_press(self):
        self.gameObject.pause = True
        self.gameObject.i2c.pause()

    def on_share_press(self):
        self.gameObject.pause = False
        self.gameObject.i2c.draw_points(self.gameObject.points)


if __name__ == "__main__":
    try:
        virtual = MAX7219()
        myGame = Tetris(32, 8)
        UI = Utilities(myGame)
        controller = MyController(interface="/dev/input/js0",
                                  connecting_using_ds4drv=False,
                                  gameObject=myGame)
        menu_thread = threading.Thread(target=controller.listen)
        menu_thread.daemon = True
        menu_thread.start()
        i2c_thread = threading.Thread(target=myGame.i2c.inside_menu)
        i2c_thread.daemon = True
        i2c_thread.start()

        while not myGame.game_over:
            UI.game_loop(virtual)

    except KeyboardInterrupt:
        print('finished by keyboard!')
        sys.exit(1)
