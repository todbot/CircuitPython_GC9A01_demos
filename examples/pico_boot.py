# Copy this as 'boot.py' in your Pico's CIRCUITPY drive
# from https://gist.github.com/Neradoc/8056725be1c209475fd09ffc37c9fad4
# Useful in case Pico locks up (which it's done a few times on me)
#
import board
import time
from digitalio import DigitalInOut,Pull

import time
led = DigitalInOut(board.LED)
led.switch_to_output()

safe = DigitalInOut(board.GP14)
safe.switch_to_input(Pull.UP)

def reset_on_pin():
	if safe.value is False:
		import microcontroller
		microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
		microcontroller.reset()

led.value = False
for x in range(16):
	reset_on_pin()
	led.value = not led.value
	time.sleep(0.1)
