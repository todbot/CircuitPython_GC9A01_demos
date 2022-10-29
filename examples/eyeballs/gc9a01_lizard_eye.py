# qteye.py - a stand-alone GC9A01 round LCD "eye" on a QTPy
# 23 Oct 2022 - @todbot / Tod Kurt
# Gator Eyes by 2022 DJDevon3
# Part of circuitpython-tricks/larger-tricks/eyeballs
# also see: https://todbot.com/blog/2022/05/19/multiple-displays-in-circuitpython-compiling-custom-circuitpython/

import time, math, random
import board, busio
import displayio
import adafruit_imageload
import gc9a01

displayio.release_displays()

dw, dh = 240,240  # display dimensions

# load our eye and iris bitmaps
eyeball_bitmap, eyeball_pal = adafruit_imageload.load("images/Lizard_Sclera.bmp")
iris_bitmap, iris_pal = adafruit_imageload.load("images/Lizard_Iris_White.bmp")
iris_pal.make_transparent(244)

# compute or declare some useful info about the eyes
iris_w, iris_h = iris_bitmap.width, iris_bitmap.height  # iris is normally 110x110
iris_cx, iris_cy = dw//2 - iris_w//2, dh//2 - iris_h//2
r = 15  # allowable deviation from center for iris

tft0_clk  = board.SCL
tft0_mosi = board.SDA
tft_L0_rst  = board.D9
tft_L0_dc   = board.D5
tft_L0_cs   = board.D6

spi0 = busio.SPI(clock=tft0_clk, MOSI=tft0_mosi)

# class to help us track eye info (not needed for this use exactly, but I find it interesting)
class Eye:
    def __init__(self, spi, dc, cs, rst, rot=0, eye_speed=0.5, twitch=1):
        display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=rst)
        display = gc9a01.GC9A01(display_bus, width=dw, height=dh, rotation=rot)
        main = displayio.Group()
        display.show(main)
        self.display = display
        self.eyeball = displayio.TileGrid(eyeball_bitmap, pixel_shader=eyeball_pal)
        self.iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x=iris_cx,y=iris_cy)
        main.append(self.eyeball)
        main.append(self.iris)
        self.x, self.y = iris_cx, iris_cy
        self.tx, self.ty = self.x, self.y
        self.next_time = time.monotonic()
        self.eye_speed = eye_speed
        self.twitch = twitch

    def update(self):
        self.x = self.x * (1-self.eye_speed) + self.tx * self.eye_speed # "easing"
        self.y = self.y * (1-self.eye_speed) + self.ty * self.eye_speed
        self.iris.x = int( self.x )
        self.iris.y = int( self.y )
        if time.monotonic() > self.next_time:
            t = random.uniform(0.25,self.twitch)
            self.next_time = time.monotonic() + t
            self.tx = iris_cx + random.uniform(-r,r)
            self.ty = iris_cy + random.uniform(-r,r)
        self.display.refresh()

# a list of all the eyes, in this case, only one
the_eyes = [
    Eye( spi0, tft_L0_dc, tft_L0_cs,  tft_L0_rst, rot=0),
]

while True:
    for eye in the_eyes:
        eye.update()
