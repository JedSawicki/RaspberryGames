from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, TINY_FONT
from luma.led_matrix.device import max7219


class MAX7219:
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=4, block_orientation=-90)
        # show_message(self.device, 'TETRIS', fill="white",
        #              font=proportional(LCD_FONT),
        #              scroll_delay=0.08)

    def full_map(self, matrix, matrix2, offset):
        tuple_list = []
        off_x, off_y = offset
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col:
                    tuple_list.append((i + off_x, j + off_y))
        with canvas(self.device) as draw:
            draw.point(tuple_list, 1)

        for i, row in enumerate(matrix2):
            for j, col in enumerate(row):
                if col:
                    tuple_list.append((i, j))
        with canvas(self.device) as draw:
            draw.point(tuple_list, 1)

    def draw_points(self, matrix, food_x, food_y):
        with canvas(self.device) as draw:
            for x in matrix:
                draw.point((x[0], x[1]), fill="white")
            # draw food
            draw.point((food_x, food_y), fill="white")
