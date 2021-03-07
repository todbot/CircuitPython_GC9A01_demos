#
# gc9a01_helloworld.py -- Simple Demo of GC9A01 Round LCD 
#
# 2021 - Tod Kurt - todbot.com
#
# Tested on QTPy (SAMD21) and Raspberry Pi Pico (RP2040)
# running CircuitPython 6.2 beta
#
# You'll need to install 'adafruit_display_text' package.
# Easiest way to do this is from Terminal:
#  circup install adafruit_display_text  
#

import time
import board
import math
import busio
import terminalio
import displayio
from adafruit_display_text import label
import todbot_gc9a01

# Release any resources currently in use for the displays
displayio.release_displays()

# # one possible Raspberry Pi Pico pinout, at "southwest" of board
# tft_clk = board.GP10 # must be a SPI CLK
# tft_mosi= board.GP11 # must be a SPI TX
# tft_rst = board.GP12
# tft_dc  = board.GP13
# tft_cs  = board.GP14
# tft_bl  = board.GP15
# spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# QT Py pinout
tft_clk  = board.SCK
tft_mosi = board.MOSI
tft_cs   = board.A3
tft_dc   = board.RX
tft_rst  = board.TX
tft_bl   = board.A2
spi = board.SPI()  

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = todbot_gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# Make the main display context
main = displayio.Group(max_size=10)
display.show(main)

# Draw a text label
text = "Hello\nWorld!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                        anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group(max_size=5, scale=2)
text_group.append(text_area) 
main.append(text_group)

# Animate the text 
theta = math.pi
r = 75
while True:
    print(time.monotonic(),"hello")
    text_group.x = 120 + int(r * math.sin(theta))
    text_group.y = 120 + int(r * math.cos(theta))
    theta -= 0.05
    time.sleep(0.05)

    
