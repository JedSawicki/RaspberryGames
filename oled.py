import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class I2C:
    def __init__(self):
        self.keep_display = True
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.disp.fill(0)
        self.disp.show()
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.x = 0
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

    def draw_menu(self):
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        self.draw.rectangle((0, 0, self.width, self.height), fill=1)
        self.draw.text((30, 5), "Let's play!", font=self.font, fill=0)
        self.disp.image(self.image)
        self.disp.show()
        time.sleep(3)
        while self.keep_display:
            # Get drawing object to draw on image.
            # Draw a black filled box to clear the image.
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw.text((35, 0), "R2: Tetris", font=self.font, fill=255)
            self.draw.text((35, 14), "L2: Snake", font=self.font, fill=255)
            self.disp.image(self.image)
            self.disp.show()
            break

    def inside_menu(self):
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        self.draw.rectangle((0, 0, self.width, self.height), fill=1)
        self.draw.text((30, 5), "Welcome", font=self.font, fill=0)
        self.disp.image(self.image)
        self.disp.show()
        time.sleep(3)
        while self.keep_display:
            # Get drawing object to draw on image.
            # Draw a black filled box to clear the image.
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw.text((35, 0), "Points:", font=self.font, fill=255)
            self.disp.image(self.image)
            self.disp.show()
            break

    def draw_points(self, points):
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((35, 0), "Points:", font=self.font, fill=255)
        self.draw.text((43, 15), f"{points}", font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

    def game_over(self, points):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((14, 0), "Game Over!", font=self.font, fill=255)
        self.draw.text((14, 15), f"Score:{points}", font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

    def pause(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((35, 0), "Pause", font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()
