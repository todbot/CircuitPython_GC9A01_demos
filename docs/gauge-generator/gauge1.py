#
# gauge1.py -- Gauge generator,
#              outputs "dial-background.bmp" file for use with CircuitPython
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

#
def draw_dial_background(draw):
    draw.stroke_color = Color('#d0d0d0') 
    draw.stroke_width = 1
    draw.fill_color = Color('#f0f0f0')
    draw.circle( (120,120), (1,120) ) # center point, perimeter point
    draw.stroke_color = Color('#e8e8e8')
    draw.circle( (120,120), (2,120) ) 
    draw.stroke_color = Color('#d8d8d8')
    draw.circle( (120,120), (5,120) ) 
    draw.stroke_color = Color('#d0d0d0')
    draw.circle( (120,120), (6,120) )
    draw.stroke_color = Color('#c8c8c8')
    draw.circle( (120,120), (7,120) )
    draw.stroke_color = Color('#c0c0c0')
    draw.circle( (120,120), (8,120) )
    draw.stroke_color = Color('#e0e0e0')
    draw.circle( (120,120), (9,120) )
    draw.stroke_color = Color('#e0e0e0')
    draw.circle( (120,120), (10,120) )
    draw.stroke_color = Color('#e0e0e0')
    draw.circle( (120,120), (11,120) )
    draw.stroke_color = Color('#c8c8c8')
    draw.circle( (120,120), (12,120) )

#
def draw_dial_ticks(draw, color, stroke_width=1.5, number_of_ticks=360,
                    start_angle=0, stop_angle=360, start_radius=100, end_radius=120):
    for i in range(number_of_ticks):
        angle = start_angle + i*(stop_angle-start_angle) /(number_of_ticks-1)
        angle_corrected = angle - 90
        angle_radians = angle_corrected / 180 * math.pi

        x1 = 120 + math.cos(angle_radians) * start_radius
        y1 = 120 + math.sin(angle_radians) * start_radius
        x2 = 120 + math.cos(angle_radians) * end_radius
        y2 = 120 + math.sin(angle_radians) * end_radius
        draw.stroke_color = color
        draw.line((x1,y1),(x2,y2))

#
def label_dial_ticks(draw, image, color, font, radius, number_ticks,
                     start_angle, stop_angle, start_label, stop_label, label_format):
    draw.fill_color = color
    draw.stroke_color = color
    draw.font = font
    draw.font_size = 22
    draw.text_alignment = 'center'
    
    for i in range(number_ticks):
        angle = start_angle + i* (stop_angle-start_angle) / (number_ticks-1)
        angle_corrected = angle - 90
        angle_radians = angle_corrected / 180.0 * math.pi
        label_value = start_label + i*(stop_label-start_label) / (number_ticks-1)
        label_string = label_format % label_value

        metrics = draw.get_font_metrics(image, label_string)
        ascent = metrics.ascender + metrics.descender
        roffset = math.sqrt( (math.cos(angle_radians) * metrics.text_width/2) *
                             (math.cos(angle_radians) * metrics.text_width/2) +
                             (math.sin(angle_radians) * ascent/2) *
                             (math.sin(angle_radians) * ascent/2))


        x1 = int(120 + math.cos(angle_radians) * (radius - roffset))
        y1 = int(120 + math.sin(angle_radians) * (radius - roffset) + ascent/2.0)
        draw.text( x1, y1, label_string)
        
# now create the image and write it out
#
with Image(width=240, height=240, background=Color('#ffffff')) as img:

    with Drawing() as draw:

        draw_dial_background(draw)
    
        draw_dial_ticks(draw, Color('#606060'), 1.5, 101, -150, 150, 97, 104) # minor
        draw_dial_ticks(draw, Color('#606060'), 1.5, 11, -150, 150, 89, 104)  # major

        label_dial_ticks(draw, img, Color("#606060"), "Oswald-Light.ttf",
                         85, 11, -150,150, 0,100, "%0.0f")

        draw.draw(img)
    
        img.type = 'palette' # CircuitPython can only do palette BMP3
        img.quantize(16)     # reduce colors for size
        img.save(filename='BMP3:dial-background.bmp')
        
