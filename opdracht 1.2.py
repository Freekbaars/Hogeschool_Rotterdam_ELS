# import lib

import board
import neopixel
import time

blauw = 0,0,255
uit = 0,0,0
knipper_tijd = 0.1


# setup

np = neopixel.NeoPixel(board.NEOPIXEL, 1)

# code
while True:
    np[0] = (blauw)
    time.sleep (knipper_tijd)
    np[0] = (uit)
    time.sleep(knipper_tijd)

