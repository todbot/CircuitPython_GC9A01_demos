#
# pointer1.py -- Gauge pointer generator,
#              outputs "pointer-red-basic.bmp" file for use with CircuitPython
#
# Translated directly from bikerglen's "gauge-generator":
#  https://github.com/bikerglen/round-lcd-gauges/tree/main/gauge-generator
#
# To use, install ImageMagic drawing API:
#  brew install imagemagick
#  pip3 install Wand
#  python3 gauage1.py
#

import math

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def draw_pointer_knub(draw, color, center_x, center_y, radius, opacity):
    draw.fill_color = color
    draw.stroke_color = Color('#333333')
    draw.stroke_opacity = 0.5
    draw.stroke_width = 2
    draw.fill_opacity = opacity
    draw.circle( (center_x, center_y), (center_x - radius, center_y))
#    draw.stroke_color=Color('#aaaaaa')
#    draw.circle( (center_x, center_y), (center_x - radius + 3, center_y))
    
def draw_pointer_needle(draw, color, stroke_width, tip_radius, tail_radius, opacity):
#    draw.stroke_opacity = 0.5
#    draw.stroke_color = Color('#333333')
#    draw.stroke_width = stroke_width+2
#    draw.line( (120, 120 + tail_radius+1), (120,120-tip_radius-1))
    draw.stroke_width = stroke_width
    draw.stroke_color = color
    draw.stroke_opacity = opacity
    draw.line( (120, 120 + tail_radius), (120,120-tip_radius))
    #draw.line( (119.5, 119.5 + tail_radius), (119.5,119.5-tip_radius))

with Image(width=240, height=240, background=Color('none')) as img:

    with Drawing() as draw:
        
#        draw_pointer_needle(draw, Color("#F45700"), 2.25, 100, 30, 1);
        draw_pointer_needle(draw, Color("#F45700"), 2.25, 102.5, 30.5, 1);
        draw_pointer_knub(draw, Color("#F45700"), 120, 120, 10, 1);
#        draw_pointer_knub(draw, Color("#F45700"), 119.5, 119.5, 10.1, 1);

        draw.draw(img)

        img.crop( 105, 15, 135, 155)

        fname = 'pointer-red-basic-30x140-c15x105'
        img.save(filename=fname+'.png')
        img.type = 'palette' # CircuitPython can only do palette BMP3
        img.quantize(16)     # reduce colors for size
        img.save(filename='BMP3:'+fname+'.bmp')



