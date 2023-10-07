import board
import time
import pwmio
import analogio
import math
import neopixel
import adafruit_hcsr04

# Definieer pinnen
x_pin = board.A0  # Analoge X-as van de joystick
y_pin = board.A1  # Analoge Y-as van de joystick

in1_pin = board.D0
in2_pin = board.D1
in3_pin = board.D2
in4_pin = board.D3

trigger_pin = board.D8
echo_pin = board.D9

# Definieer NeoPixel
num_pixels = 1
neopixel_pin = board.NEOPIXEL
pixels = neopixel.NeoPixel(neopixel_pin, num_pixels, brightness=0.3)

# Definieer de drempelwaarde als een aanpasbare variabele
drempel_percentage = 5 / 100  # Stel hier je gewenste drempelwaarde in
buffer_afstand = 10  # Stel hier de gewenste bufferafstand in (in centimeters)
achteruit_rijd_tijd = 1.0  # Tijd om achteruit te rijden in seconden

# Pin-initialisatie
in1 = pwmio.PWMOut(in1_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig
in2 = pwmio.PWMOut(in2_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig
in3 = pwmio.PWMOut(in3_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig
in4 = pwmio.PWMOut(in4_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig

# Joystick-initialisatie
x_axis = analogio.AnalogIn(x_pin)
y_axis = analogio.AnalogIn(y_pin)

# Sonarsensor-initialisatie
sonar = adafruit_hcsr04.HCSR04(trigger_pin, echo_pin)

# Variabele voor NeoPixel-knipperen
neo_pixel_on = False

# Functies voor beweging
def drive_motors(left_speed, right_speed):
    left_speed = min(max(-max_speed, left_speed), max_speed)
    right_speed = min(max(-max_speed, right_speed), max_speed)

    global neo_pixel_on  # Gebruik de globale variabele

    if abs(x_normalized) < drempel_percentage and abs(y_normalized) < drempel_percentage:
        # Als de joystick binnen de drempel valt, schakel NeoPixel in rood in en laat deze knipperen
        neo_pixel_on = not neo_pixel_on  # Toggle de status van de NeoPixel
        if neo_pixel_on:
            pixels.fill((255, 0, 0))  # Rood
        else:
            pixels.fill((0, 0, 0))  # Uit

        # Schakel de motoren uit
        left_speed = 0
        right_speed = 0
    else:
        # Zo niet, schakel NeoPixel uit
        neo_pixel_on = False
        if left_speed != 0 or right_speed != 0:
            pixels.fill((0, 0, 255))  # Blauw
        else:
            pixels.fill((0, 0, 0))  # Uit

    if left_speed >= 0:
        left_FWD(left_speed)
    else:
        left_BWD(-left_speed)

    if right_speed >= 0:
        right_FWD(right_speed)
    else:
        right_BWD(-right_speed)

def left_FWD(DutyF):
    set_pwm_duty_cycle(in1, DutyF)
    set_pwm_duty_cycle(in2, 0)

def left_BWD(DutyB):
    set_pwm_duty_cycle(in1, 0)
    set_pwm_duty_cycle(in2, DutyB)

def right_FWD(DutyF):
    set_pwm_duty_cycle(in3, DutyF)
    set_pwm_duty_cycle(in4, 0)

def right_BWD(DutyB):
    set_pwm_duty_cycle(in3, 0)
    set_pwm_duty_cycle(in4, DutyB)

def set_pwm_duty_cycle(pwm_pin, duty_cycle):
    max_duty_cycle = 2 ** 16 - 1
    if 0 <= duty_cycle <= max_duty_cycle:
        pwm_pin.duty_cycle = int(duty_cycle)
    else:
        if duty_cycle < 0:
            pwm_pin.duty_cycle = 0
        else:
            pwm_pin.duty_cycle = max_duty_cycle

def stop_if_obstacle():
    try:
        distance = sonar.distance
        if distance is not None and distance < buffer_afstand:
            # Als de gemeten afstand kleiner is dan de buffer_afstand, stop de auto en rijd achteruit
            drive_motors(0, 0)
            rij_naar_achteren()
    except RuntimeError as e:
        # Als er een time-out optreedt, behandel deze dan hier
        print("Fout bij het meten van de afstand:", e)

def rij_naar_achteren():
    left_speed = -max_speed  # Achteruit rijden
    right_speed = -max_speed  # Achteruit rijden
    drive_motors(left_speed, right_speed)  # Rijd achteruit
    time.sleep(achteruit_rijd_tijd)  # Wacht de opgegeven tijd
    drive_motors(0, 0)  # Stop de motoren

# Hoofdcode
while True:
    x_value = x_axis.value
    y_value = y_axis.value

    print("X-waarde:", x_value)
    print("Y-waarde:", y_value)

    # Bereken de snelheden op basis van de joystickwaarden
    x_center = 32000
    y_center = 32000
    max_speed = 2**16 - 1

    x_normalized = (x_value - x_center) / x_center
    y_normalized = (y_value - y_center) / x_center

    forward_speed = max_speed * abs(y_normalized)
    turn_speed = max_speed * x_normalized

    if y_normalized < 0:  # Omgekeerde polariteit voor achteruit
        left_speed = forward_speed - turn_speed
        right_speed = forward_speed + turn_speed
    else:
        left_speed = -forward_speed - turn_speed
        right_speed = -forward_speed + turn_speed

    # Stuur de motoren aan op basis van de snelheden
    drive_motors(left_speed, right_speed)
    
    # Stop de auto als een obstakel wordt gedetecteerd
    stop_if_obstacle()

    time.sleep(0.1)  # Kleinere pauze om de responsiviteit te verhogen
    
