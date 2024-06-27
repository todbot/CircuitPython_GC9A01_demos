#
# gc9a01_hellocircles.py -- Simple Demo of GC9A01 Round LCD 
#
# 2021 - Tod Kurt - todbot.com
#
# Tested on QTPy M0 (SAMD21), QTPy RP2040, ItsyBitsy M4,
# Raspberry Pi Pico (RP2040) running CircuitPython 7.
#
# You'll need to install 'adafruit_display_text' and 'gc9a01' library.
# Easiest way to do this is from Terminal:
#  circup install adafruit_display_text gc9a01
#

import time
import board
import math
import random
import busio
import terminalio
import displayio
from vectorio import Rectangle, Circle, Polygon
from adafruit_display_text import label
import gc9a01

# Release any resources currently in use for the displays
displayio.release_displays()

# attempt to auto-detect board type
import os
board_type = os.uname().machine

if 'QT Py M0 Haxpress' in board_type or 'QT Py RP2040' in board_type:
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    tft_rst  = board.TX
    tft_dc   = board.RX
    tft_cs   = board.A3
    tft_bl   = board.A2
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
elif 'Adafruit Feather M4 Express with samd51j19' in board_type:
    tft_clk  = board.SCL
    tft_mosi = board.SDA
    tft_rst  = board.D9
    tft_dc   = board.D6
    tft_cs   = board.D5
    tft_bl   = board.A3  # optional
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
elif 'ItsyBitsy M4' in board_type:
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    tft_rst  = board.MISO
    tft_dc   = board.D2
    tft_cs   = board.A5
    tft_bl   = board.A3  # optional
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
elif 'Pico' in board_type:
    # Raspberry Pi Pico pinout, one possibility, at "southwest" of board
    tft_clk = board.GP10 # must be a SPI CLK
    tft_mosi= board.GP11 # must be a SPI TX
    tft_rst = board.GP12
    tft_dc  = board.GP13
    tft_cs  = board.GP14
    tft_bl  = board.GP15
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
elif 'Waveshare RP2040-LCD-1.28 with rp2040' in board_type:
    tft_clk = board.LCD_CLK
    tft_mosi = board.LCD_DIN
    tft_rst = board.LCD_RST
    tft_dc = board.LCD_DC
    tft_cs = board.LCD_CS
    tft_bl = board.LCD_BL
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
else:
    print("ERROR: Unknown board!")

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# Make the main display context
main = displayio.Group()
display.root_group = main

for i in range(15):
    sx = random.randint(0, 240)
    sy = random.randint(0, 240)
    circ_palette = displayio.Palette(1)
    circ_palette[0] =  (random.randint(0,0xFF), 0, random.randint(0,0xFF))
    main.append(Circle(pixel_shader=circ_palette, radius=30, x=sx, y=sy))

# Draw a text label
text = "Hello\nWorld!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                        anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group(scale=2)
text_group.append(text_area) 
main.append(text_group)

display.auto_refresh = False
# Animate the text 
theta = math.pi
r = 75
while True:
    print(time.monotonic(),"hello")
    i = random.randint(0,15)
    main[i].x = (main[i].x + 5) % 240
    text_group.x = 120 + int(r * math.sin(theta))
    text_group.y = 120 + int(r * math.cos(theta))
    display.refresh()
    theta -= 0.05
    time.sleep(0.01)
