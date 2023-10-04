import time
import board
import adafruit_hcsr04

trigger_pin = board.D2
echo_pin = board.D3 


sonar = adafruit_hcsr04.HCSR04(trigger_pin, echo_pin)

while True:
    try:
        print((sonar.distance,))
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)