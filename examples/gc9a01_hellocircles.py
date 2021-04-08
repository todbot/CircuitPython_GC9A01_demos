#
# gc9a01_hellocircles.py -- Simple Demo of GC9A01 Round LCD 
#
# 2021 - Tod Kurt - todbot.com
#
# Tested on QTPy (SAMD21), ItsyBitsy M4, Raspberry Pi Pico (RP2040)
# running CircuitPython 6.2 beta
#
# Copy this file to be your CIRCUITPY's "code.py", like:
#  cp gc9a01_hellocircles.py /Volumes/CIRCUITPY/code.py
#
# You'll need to install 'adafruit_display_text' library.
# Easiest way to do this is from Terminal:
#  circup install adafruit_display_text
#
# You'll need to install the 'gc9a01' library.
# You can get that from the "Circuit_Python_Community" bundle:
#  https://github.com/adafruit/CircuitPython_Community_Bundle/releases
# Unzip it and copy the "gc9a01.mpy" to the lib folder, like:
#  cp ~/Downloads/circuitpython-community-bundle-6.x-mpy-20210403/lib/gc9a01.mpy /Volumes/CIRCUITPY/lib
#

import time
import board
import math
import random
import busio
import terminalio
import displayio
from vectorio import Rectangle, Circle, Polygon, VectorShape
from adafruit_display_text import label
import gc9a01

# Release any resources currently in use for the displays
displayio.release_displays()

# attempt to auto-detect board type
import os
board_type = os.uname().machine

if 'QT Py M0 Haxpress' in board_type:
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    tft_rst  = board.TX
    tft_dc   = board.RX
    tft_cs   = board.A3
    tft_bl   = board.A2
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

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# Make the main display context
main = displayio.Group(max_size=20)
display.show(main)

for i in range(15):
    sx = random.randint(0, 240)
    sy = random.randint(0, 240)
    circ = Circle(30)
    circ_palette = displayio.Palette(2)
    circ_palette.make_transparent(0)
    circ_palette[1] =  (random.randint(0,0xFF), 0, random.randint(0,0xFF))
    main.append(VectorShape(shape=circ, x=sx,y=sy, pixel_shader=circ_palette))

# Draw a text label
text = "Hello\nWorld!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                        anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group(max_size=5, scale=2)
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

    
