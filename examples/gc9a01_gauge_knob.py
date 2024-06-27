# gc9a01_dial_knob.py -- Demonstrate round LCD as a gauge, controlled by a pot knob
#
# 2021 - Tod Kurt - todbot.com
#
# Tested on QTPy RP2040, ItsyBitsy M4,
# Raspberry Pi Pico (RP2040) running CircuitPython 7
#
# You'll need to install 'adafruit_display_text', 'adafruit_imageload'
# and 'gc9a01' library.
# Easiest way to do this is from Terminal:
#  circup install adafruit_display_text adafruit_imageload gc9a01
#

import time
import math
import board
import busio
import displayio
import bitmaptools
import terminalio
from analogio import AnalogIn
import adafruit_imageload
from adafruit_display_text import label
import gc9a01

# change these as you like, keep the pointer center at 15,105
dial_background_filename = '/imgs/dial-background.bmp'
pointer_filename = '/imgs/pointer-red-basic-30x140-c15x105.bmp'
legend_text = "PERCENT\nAWESOME"

displayio.release_displays()

import os
board_type = os.uname().machine

if 'QT Py M0' in board_type or 'QT Py RP2040' in board_type: 
    # QT Py pinout
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    tft_rst  = board.TX
    tft_dc   = board.RX
    tft_cs   = board.A3
    tft_bl   = board.A2 # optional
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
elif 'ItsyBitsay M4' in board_type:
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    tft_rst  = board.MISO
    tft_dc   = board.D2
    tft_cs   = board.A5
    tft_bl   = board.A3  # optional
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
elif 'Pico' in board_type:
    # # one pinout, on "southeast" side of Pico board 
    # tft_clk = board.GP18
    # tft_mosi= board.GP19
    # tft_rst = board.GP20
    # tft_dc  = board.GP16
    # tft_cs  = board.GP17
    # tft_bl  = board.GP21
    # spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

    # another pinout, on "southwest" of Pico board
    tft_clk = board.GP10
    tft_mosi= board.GP11
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

# Analog knob to control dial
analog_in = AnalogIn(board.A1)

# Create displayio bus and display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=240,
                        backlight_pin=tft_bl, auto_refresh=False)

# Create main display group and add it to the display
main = displayio.Group()
display.root_group = main

# 240x240 dial background
bg_bitmap,bg_pal = adafruit_imageload.load(dial_background_filename)
bg_tile_grid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_pal)
main.append(bg_tile_grid)

# Text legend
text_area = label.Label(terminalio.FONT, text=legend_text, line_spacing=0.9, color=0x000000, anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group(scale=1, x=120, y=155)
text_group.append(text_area)
main.append(text_group)  # Subgroup for text scaling

# 30x140 pointer
bitmap_pointer, palette_pointer = adafruit_imageload.load(pointer_filename, bitmap=displayio.Bitmap,palette=displayio.Palette)
palette_pointer.make_transparent(0)

# Blank bitmap the same size as the pointer bitmap
bitmap_pointer_blank = displayio.Bitmap(bitmap_pointer.width, bitmap_pointer.height, 1)# len(palette_pointer))
#bitmap_pointer_blank.fill(0)

# Transparent overlay that is "scribbled" into by rotozoom
# to create rotated version of pointer
bitmap_scribble = displayio.Bitmap(display.width, display.height, len(palette_pointer))
tile_grid = displayio.TileGrid(bitmap_scribble, pixel_shader=palette_pointer)
main.append(tile_grid)

# Do initial draw
display.refresh()

print("Hello World!")

# simple range mapper, like Arduino map()
def map_range(s, a, b):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

# for dial 'dial-percenti.bmp', range is kinda:
# 0% - 100% => + 2.6 - -2.6
def percent_to_theta(p):
    return map_range(p,  (0.0,1.0), (-2.6, 2.6) )

percent = 0.0
last_time = time.monotonic()
while True:
    percent = map_range( analog_in.value, (200,65400), (1,0))
    theta = percent_to_theta(percent)
    
    print("dt:",time.monotonic()-last_time,"theta:", theta, int(percent*100))
    last_time = time.monotonic()

    # erasing the entire bitmap is slow (~1fps, because of transparency I think)
    # instead we erase just the region we modified, after refresh below
    # bitmap_scribble.fill(0)
    
    # offset rotation point (15,105) for bitmap_pointer's axis of rotation
    bitmaptools.rotozoom( bitmap_scribble, bitmap_pointer, angle = theta, px=15,py=105)
    
    display.refresh()

    # after refresh, now "erase" the rotated pointer by doing a
    # rotozom of a "blank" bitmap with only transparency
    bitmaptools.rotozoom( bitmap_scribble, bitmap_pointer_blank, angle = theta, px=15,py=105)
