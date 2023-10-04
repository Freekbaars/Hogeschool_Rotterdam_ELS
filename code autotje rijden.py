import board
import time
import pwmio
import analogio

# Definieer pinnen
x_pin = board.A0  # Analoge X-as van de joystick
y_pin = board.A1  # Analoge Y-as van de joystick

in1_pin = board.D0
in2_pin = board.D1
in3_pin = board.D2
in4_pin = board.D3


# Pin-initialisatie
in1 = pwmio.PWMOut(in1_pin)
in2 = pwmio.PWMOut(in2_pin)
in3 = pwmio.PWMOut(in3_pin)
in4 = pwmio.PWMOut(in4_pin)

# Joystick-initialisatie
x_axis = analogio.AnalogIn(x_pin)
y_axis = analogio.AnalogIn(y_pin)

# Functies voor beweging
def drive_motors(left_speed, right_speed):
    left_FWD(left_speed)
    right_FWD(right_speed)

def left_FWD(DutyF):
    in1.duty_cycle = int(DutyF * (2**16-1))
    in2.duty_cycle = 0

def left_BWD(DutyB):
    in1.duty_cycle = 0
    in2.duty_cycle = int(DutyB * (2**16-1))

def right_FWD(DutyF):
    in3.duty_cycle = int(DutyF * (2**16-1))
    in4.duty_cycle = 0

def right_BWD(DutyB):
    in3.duty_cycle = 0
    in4.duty_cycle = int(DutyB * (2**16-1))

# Hoofdcode
while True:
    x_value = x_axis.value
    y_value = y_axis.value

    print("X-waarde:", x_value)
    print("Y-waarde:", y_value)

    #left_speed = y_value
    #right_speed = y_value

    #if x_value < 0.5:
    #    left_speed *= 2.0 * x_value
    #else:
    #    right_speed *= 2.0 * (1.0 - x_value)

    #drive_motors(left_speed, right_speed)

    time.sleep(0.2)  # Kleinere pauze om de responsiviteit te verhogen
