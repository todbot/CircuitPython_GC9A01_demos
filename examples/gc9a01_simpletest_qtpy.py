#
# works on QTPy

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import terminalio
import displayio
from adafruit_display_text import label
import todbot_gc9a01

# Release any resources currently in use for the displays
displayio.release_displays()

# QT Py pinout
spi = board.SPI()
tft_cs = board.A3
tft_dc = board.RX
tft_rst = board.TX
tft_bl = board.A2

backlight = DigitalInOut(tft_bl)
backlight.direction = Direction.OUTPUT
backlight.value = True

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = todbot_gc9a01.GC9A01(display_bus, width=240, height=240)

# Make the display context
main = displayio.Group(max_size=10)
display.show(main)

# Draw a text label
text_group = displayio.Group(max_size=5, scale=2, x=50, y=100)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
main.append(text_group)

print("what")

while True:
    print(time.monotonic(),"hello")
    time.sleep(1)

    
