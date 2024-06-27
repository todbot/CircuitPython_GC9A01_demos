import time, math, random
import board, busio
import displayio, terminalio
import rainbowio, vectorio
import gc9a01
from adafruit_display_text import bitmap_label as label

dw,dh = 240,240  # display width,height

displayio.release_displays()
# Raspberry Pi Pico pinout, one possibility, at "southeast" of board
tft_clk = board.GP18 # must be a SPI CLK
tft_mosi= board.GP19 # must be a SPI TX
tft_rst = board.GP21
tft_dc  = board.GP16
tft_cs  = board.GP17

spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=dw, height=dh, rotation=270)
maingroup = displayio.Group()  # a main group that holds everything
display.root_group = maingroup # put it on the display

# draw cirlces
for i in range(15):
    sx = random.randint(0, dw)
    sy = random.randint(0, dh)
    pal = displayio.Palette(1)
    pal[0] =  rainbowio.colorwheel( random.randint(180,240) )  # 240 is a coincidence here
    #s0 = vectorio.Circle(pixel_shader=pal0, radius=30, x=sx, y=sy)
    s0 = vectorio.Circle(pixel_shader=pal, radius=30, x=sx, y=sy) 
    maingroup.append(s0)

# Draw a text label
text_area = label.Label(terminalio.FONT, text="Hellow\nWorld!", color=0xFFFF00, scale=2,
                        anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group() # put in a group so anchor_position works correctly
text_group.append(text_area)
maingroup.append(text_group)

# Animate the text 
theta = math.pi
r = 75
while True:
    print(time.monotonic(),"hello")
    i = random.randint(0,15)
    maingroup[i].x = (maingroup[i].x + 5) % 240
    text_group.x = 120 + int(r * math.sin(theta))
    text_group.y = 120 + int(r * math.cos(theta))
    display.refresh( target_frames_per_second=20 )
    theta -= 0.05

