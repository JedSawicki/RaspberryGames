# RaspberryGames
A simple project to make MAX7219 and oled displays playable.
## Requirements:
- Python 3.9
- SPI and I2C protocols enabled on Raspberry
### Libraries
- pyPS4Controller
- luma led_matrix library(led matrix device): https://github.com/rm-hull/luma.led_matrix
- Adafruit_CircuitPython_SSD1306(oled device): https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
### Devices(ex. from botland)
- OLED display 0,96'': https://botland.store/displays-and-screens/8866-oled-display-blue-graphic-096-128x64px-i2c-blue-5904422337421.html

![oled](https://user-images.githubusercontent.com/95547700/157290690-e63f2071-bf09-490c-aea8-87aaa0ef80c6.png)


- LED Matrix 32x8 using MAX7219

![matrix](https://user-images.githubusercontent.com/95547700/157290932-69fee955-8b1f-4c92-85d4-0b7cdfa9516c.png)

- Ps4 Dualshock Gamepad connected with usb cable

### Connecting devices
Example of connecting the devices showed below

![scheme](https://user-images.githubusercontent.com/95547700/157293069-0e42e673-a4e6-4017-b32a-c1aabb55152b.png)

Where Max7219 is using:
- 5V
- GND
- MOSI
- SCLK
- CS

Oled display:
- 3.3V
- GND
- SDA
- SCL

### Controls
Tetris game:
- Movement by arrows
- X - drop block
- Triangle - Rotate block
- Circle - Exit game
- Options button - pause
- Share button - resume

Snake game:
- Movement by arrows
- Circle - Exit game
- Options button - pause
- Share button - resume

To run the game, use the console:

```
$ cd ../RaspberryGames
$ python tetris.py
$ python snake.py
```
In case your led matrix is another size, just simply change the code at the bottom of a chosen game:

![capture](https://user-images.githubusercontent.com/95547700/157291935-116dc28a-5686-40de-b30c-7870a74bd9f0.PNG)


### Presentation
![tt](https://user-images.githubusercontent.com/95547700/157293502-20ad5b7a-7566-4950-82ec-849c35ac83fb.jpg)

![IMG_20220202_215041](https://user-images.githubusercontent.com/95547700/157293608-5b83b4e5-0588-4cd5-a13a-75ea710cc3c2.jpg)

