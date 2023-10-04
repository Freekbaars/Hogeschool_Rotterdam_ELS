# import lib

import board
import neopixel


blauw = 0,0,255

# setup

np = neopixel.NeoPixel(board.NEOPIXEL, 1)

# code
while True:
    np[0] = (blauw)