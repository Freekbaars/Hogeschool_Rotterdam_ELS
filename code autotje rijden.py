import board
import time
import pwmio
import analogio
import math

# Definieer pinnen
x_pin = board.A0  # Analoge X-as van de joystick
y_pin = board.A1  # Analoge Y-as van de joystick

in1_pin = board.D0
in2_pin = board.D1
in3_pin = board.D2
in4_pin = board.D3

# Pin-initialisatie
in1 = pwmio.PWMOut(in1_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig
in2 = pwmio.PWMOut(in2_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig
in3 = pwmio.PWMOut(in3_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig
in4 = pwmio.PWMOut(in4_pin, frequency=1000, duty_cycle=0)  # Pas de frequentie aan indien nodig

# Joystick-initialisatie
x_axis = analogio.AnalogIn(x_pin)
y_axis = analogio.AnalogIn(y_pin)

# Functies voor beweging
def drive_motors(left_speed, right_speed):
    left_FWD(left_speed)
    right_FWD(right_speed)

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
    y_normalized = (y_value - y_center) / y_center

    left_speed = max_speed * y_normalized - max_speed * x_normalized
    right_speed = max_speed * y_normalized + max_speed * x_normalized

    # Zorg ervoor dat de snelheid binnen het geldige bereik ligt
    left_speed = min(max_speed, max(-max_speed, left_speed))
    right_speed = min(max_speed, max(-max_speed, right_speed))

    # Stuur de motoren aan op basis van de snelheden
    drive_motors(left_speed, right_speed)

    time.sleep(0.1)  # Kleinere pauze om de responsiviteit te verhogen
