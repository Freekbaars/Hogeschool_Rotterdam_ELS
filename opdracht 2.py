import board
import digitalio
import time

# pin out

wit = board.D13
rood = board.D12
groen = board.D11

#dev variables
knipper_tijd = 0.1



# code

#wit
LEDW = digitalio.DigitalInOut(wit)
LEDW.direction = digitalio.Direction.OUTPUT

#rood
LEDR = digitalio.DigitalInOut(rood)
LEDR.direction = digitalio.Direction.OUTPUT

#groen
LEDG = digitalio.DigitalInOut(groen)
LEDG.direction = digitalio.Direction.OUTPUT


while True:
    LEDW.value = True
    time.sleep(knipper_tijd)
    LEDW.value = False
    time.sleep(knipper_tijd)

    LEDR.value = True
    LEDG.value = True
