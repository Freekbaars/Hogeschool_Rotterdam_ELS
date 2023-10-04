import board
import time
from analogio import AnalogIn

potmeter = board.A0

potmeter = AnalogIn(potmeter)

while True:
    print((potmeter.value/65520*100,))
    time.sleep(0.1)