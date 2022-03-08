import random
import sys
import threading
import time

from pyPS4Controller.controller import Controller

from MAX7219 import MAX7219
from oled import I2C


class Snake:
    def __init__(self, y, x):
        # starting point
        self.point_x = 3
        self.point_y = 8
        # board size
        self.x = x
        self.y = y
        self.game_over = False
        self.game_speed = 0.3
        self.pause = False
        self.points = 0
        self.i2c = I2C()

        self.snake = [[self.point_y, self.point_x]]
        self.length_of_snake = 1
        self.snake_direction = None

        self.x_change = 0
        self.y_change = 0

        self.food_y, self.food_x = self.generate_food()

    def defeat_checker(self, snake_head, snake_list):
        if snake_head[1] >= self.x or snake_head[1] < 0 or snake_head[0] >= self.y or snake_head[0] < 0:
            self.game_over = True

        for x in snake_list[:-1]:
            if x == snake_head:
                self.game_over = True

    def generate_food(self):
        self.food_x = (random.randrange(0, self.x-1))
        self.food_y = (random.randrange(0, self.y-1))
        return self.food_y, self.food_x

    def game_loop(self, virtual):
        # loop for the game
        # refreshing speed
        time.sleep(self.game_speed)
        while self.pause and not self.game_over:
            time.sleep(1)
        snake_head = [self.point_y, self.point_x]

        self.defeat_checker(snake_head, self.snake)
        # after that move the snake
        self.point_x += self.x_change
        self.point_y += self.y_change

        self.snake.append(snake_head)

        if len(self.snake) > self.length_of_snake:
            del self.snake[0]

        virtual.draw_points(self.snake, self.food_y, self.food_x)
        if self.point_x == self.food_x and self.point_y == self.food_y:
            print('Yummy!')
            self.generate_food()
            self.length_of_snake += 1
            self.points += 1
            self.i2c.draw_points(self.points)


class MyController(Controller):
    def __init__(self, **kwargs):
        if 'gameObject' in kwargs:
            self.gameObject = kwargs.get('gameObject')
            kwargs.pop('gameObject')
        Controller.__init__(self, **kwargs)

    def on_down_arrow_press(self):
        if self.gameObject.snake_direction != 'Up':
            self.gameObject.x_change = 0
            self.gameObject.y_change = 1
            self.gameObject.snake_direction = 'Down'

    def on_up_arrow_press(self):
        if self.gameObject.snake_direction != 'Down':
            self.gameObject.x_change = 0
            self.gameObject.y_change = -1
            self.gameObject.snake_direction = 'Up'

    def on_right_arrow_press(self):
        if self.gameObject.snake_direction != 'Left':
            self.gameObject.x_change = -1
            self.gameObject.y_change = 0
            self.gameObject.snake_direction = 'Right'

    def on_left_arrow_press(self):
        if self.gameObject.snake_direction != 'Right':
            self.gameObject.x_change = 1
            self.gameObject.y_change = 0
            self.gameObject.snake_direction = 'Left'

    def on_options_press(self):
        self.gameObject.pause = True
        self.gameObject.i2c.pause()

    def on_share_press(self):
        self.gameObject.pause = False
        self.gameObject.i2c.draw_points(self.gameObject.points)

    def on_circle_press(self):
        self.gameObject.game_over = True
        self.gameObject.game_speed = 0.03
        self.gameObject.i2c.game_over(self.gameObject.points)


if __name__ == "__main__":
    try:
        virtual = MAX7219()
        myGame = Snake(32, 8)
        controller = MyController(interface="/dev/input/js0",
                                  connecting_using_ds4drv=False, gameObject=myGame)

        menu_thread = threading.Thread(target=controller.listen)
        menu_thread.daemon = True
        menu_thread.start()

        i2c_thread = threading.Thread(target=myGame.i2c.inside_menu)
        i2c_thread.daemon = True
        i2c_thread.start()
        while not myGame.game_over:
            myGame.game_loop(virtual)

        # virtual.draw_points(point)

    except KeyboardInterrupt:
        print('finished by keyboard!')
        sys.exit(1)
