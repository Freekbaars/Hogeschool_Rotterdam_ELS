import board
import time
import pwmio
import digitalio

#def pins

potmeter = board.A0
in1_pin = board.D0
in2_pin = board.D1
in3_pin = board.D2
in4_pin = board.D3

#pin initialization

in1 = pwmio.PWMOut(in1_pin)
in2 = pwmio.PWMOut(in2_pin)
in3 = pwmio.PWMOut(in3_pin)
in4 = pwmio.PWMOut(in4_pin)



#def functions

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


#def code

while True:
    left_FWD(0.8)
    right_FWD(0.8)

    time.sleep(1)

    left_BWD(0.8)
    right_BWD(0.8)

    time.sleep(1)