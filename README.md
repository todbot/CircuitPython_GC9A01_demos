# todbot_CircuitPython_GC9A01

CircuitPython driver for GC9A01 round LCDs

<img width=400 src="./docs/gc9a01_demo1.jpg" />
<img width=400 src="./docs/gc9a01_demo2.jpg" />



## Usage

```py
import board
import displayio
import todbot_gc9a01

# Raspberry Pi Pico pinout, one possibility, at "southwest" of board
tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP13
tft_cs  = board.GP14
tft_bl  = board.GP15
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = todbot_gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# ... normal circuitpython displayio stuff
```


