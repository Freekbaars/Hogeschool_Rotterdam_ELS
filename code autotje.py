#project: autotje ELS
#author: Freek Baars
#date: 31-08-2023
#version: 0.1
#description: autotje dat kan rijden en stoppen voor obstakels
#___________________________________________________________


#def libs
import board
import time
from time import sleep_ms
import pwmio
import digitalio
import pygame

#sonar
import adafruit_hcsr04


#___________________________________________________________


#variable
vijlighijdsmarge = 0.5

# maxSpeed = 1024 !!!
minSpeed = 300
midSpeed = 700
maxSpeed = 1024
speed = midSpeed
action = 0


#___________________________________________________________


#def pins

#motor
in1_pin = board.D0
in2_pin = board.D1
in3_pin = board.D2
in4_pin = board.D3

#echo
trigger_pin = board.D2
echo_pin = board.D3 


#___________________________________________________________


#pin activation

#motor
IN1 = pwmio.PWMOut(in1_pin)
IN2 = pwmio.PWMOut(in2_pin)
IN3 = pwmio.PWMOut(in3_pin)
IN4 = pwmio.PWMOut(in4_pin)

#sonar
sonar = adafruit_hcsr04.HCSR04(trigger_pin, echo_pin)


#___________________________________________________________
#webserver

html = """<!DOCTYPE html>
<html>
<head>
<title>Car</title>
<style>
body {background-color: black}
h1 {color:red}
button {
        color: white;
        height: 200px;
        width: 200px;
        background: #4CAF50;
        border: 3px solid #4CAF50; /* Green */
        border-radius: 50%;
        font-size: 250%;
        position: center;
}
</style>
</head>
<body>
<center>
<form>
<div><button name="CMD" value="l" type="submit">L</button>
<button name="CMD" value="forward" type="submit">Forward</button>
<button name="CMD" value="r" type="submit">R</button></div>
<div><button name="CMD" value="left" type="submit">Ls</button>
<button name="CMD" value="stop" type="submit">Stop</button>
<button name="CMD" value="right" type="submit">Rs</button></div>
<div><button name="CMD" value="back" type="submit">Back</button></div>
<div><button name="CMD" value="slow" type="submit">Slow</button>
<button name="CMD" value="mid" type="submit">Mid</button>
<button name="CMD" value="fast" type="submit">Fast</button>
<button name="CMD" value="auto" type="submit">Auto</button></div>
</form>
</center>
</body>
</html>
"""

#___________________________________________________________
#def functions

def setMotor(MotorPin, val):
  MotorPin.freq(50)
  MotorPin.duty(val)

# rijden

def stop(t=0):
  setMotor(IN1, 0)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def forward(t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)


def back(t=0):
  setMotor(IN1, 0)
  setMotor(IN2, speed)
  setMotor(IN3, 0)
  setMotor(IN4, speed)
  if t > 0 :
    sleep_ms(t)


def left (t=0):
  setMotor(IN1, 0)
  setMotor(IN2, speed)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)


def right (t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, speed)
  if t > 0 :
    sleep_ms(t)

def left_cruise (t=0):
  setMotor(IN1, 0)
  setMotor(IN2, 0)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def right_cruise (t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)


def forward_distance():
    return sonar.distance_cm()

def localControl () :
    global auto, action, speed
    if action == 0:
        stop ()
    elif action == 1:
        forward()
    elif action == 2:
        back()
    elif action == 3:
        left()
    elif action == 4:
        right()
    elif action == 5:
        left_cruise()
    elif action == 6:
        right_cruise()
        
        

def remoteControl () :
    global auto, s, action, speed
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)

    if request.find('/?CMD=forward') == 6:
        print('+forward')
        action = 1
    elif request.find('/?CMD=back') == 6:
        print('+back')
        action = 2
    elif request.find('/?CMD=left') == 6:
        print('+left')
        action = 3
    elif request.find('/?CMD=right') == 6:
        print('+right')
        action = 4
    elif request.find('/?CMD=l') == 6:
        print('+L')
        action = 5
    elif request.find('/?CMD=r') == 6:
        print('+R')
        action = 6
    elif request.find('/?CMD=stop') == 6:
        print('+stop')
        action = 0
    elif request.find('/?CMD=fast') == 6:
        print('+fast=')
        speed = maxSpeed
        print (speed)
    elif request.find('/?CMD=slow') == 6:
        print('+slow=')
        speed = minSpeed
        print (speed)
    elif request.find('/?CMD=mid') == 6:
        print('+mid=')
        speed = midSpeed
        print (speed)
    elif request.find('/?CMD=man') == 6:
        auto=False
        action = 0
        print('+manual=')
    elif request.find('/?CMD=auto') == 6:
        auto=True
        action = 0
        print('+autoDrive')

    if action == 0:
        stop ()
    elif action == 1:
        forward()
    elif action == 2:
        back()
    elif action == 3:
        left()
    elif action == 4:
        right()
    elif action == 5:
        left_cruise()
    elif action == 6:
        right_cruise()

    response = html
    conn.send(response)
    conn.close()


def yojsticControl():
    global auto, action, speed
    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if joystick.get_axis(1) < -0.5:
                    print('+forward')
                    action = 1
                elif joystick.get_axis(1) > 0.5:
                    print('+back')
                    action = 2
                elif joystick.get_axis(0) < -0.5:
                    print('+left')
                    action = 3
                elif joystick.get_axis(0) > 0.5:
                    print('+right')
                    action = 4
                else:
                    print('+stop')
                    action = 0
            elif event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(0):
                    print('+L')
                    action = 5
                elif joystick.get_button(1):
                    print('+R')
                    action = 6
                elif joystick.get_button(2):
                    print('+fast=')
                    speed = maxSpeed
                    print(speed)
                elif joystick.get_button(3):
                    print('+slow=')
                    speed = minSpeed
                    print(speed)
                elif joystick.get_button(4):
                    print('+mid=')
                    speed = midSpeed
                    print(speed)
                elif joystick.get_button(5):
                    auto = False
                    action = 0
                    print('+manual=')
                elif joystick.get_button(6):
                    auto = True
                    action = 0
                    print('+autoDrive')


while True
    if auto:
        if forward_distance() > vijlighijdsmarge:
            forward()
        else:
            stop()

            