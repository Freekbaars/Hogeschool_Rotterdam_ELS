import	board
import socket
import machine
import time
from machine import Pin, PWM, ADC, time_pulse_us
from time import sleep, sleep_us, sleep_ms
import hcsr04
from hcsr04 import HCSR04

wifissid = 'yourwifissid'
wifipass = 'yourwifipass'

sensor = HCSR04(trigger_pin=13, echo_pin=15)

servo_right = 30
servo_centre = 77
servo_left = 120
servo_delay = 250 #ms
servo = machine.PWM(machine.Pin(2), freq=50)

IN1 = PWM(Pin(14))
IN2 = PWM(Pin(12))
IN3 = PWM(Pin(5))
IN4 = PWM(Pin(4))

minSpeed = 300
midSpeed = 700
maxSpeed = 1024
speed = midSpeed
action = 0

auto=False

def forward_distance () :
  servo.duty(servo_centre) #centre
  return sensor.distance_cm()

def right_distance () :
  servo.duty(servo_right)
  sleep_ms(servo_delay)
  return sensor.distance_cm()

def left_distance () :
  servo.duty(servo_left)
  sleep_ms(servo_delay)
  return sensor.distance_cm()

def setMotor(MotorPin, val):
  MotorPin.freq(50)
  MotorPin.duty(val)





#HTML to send to browsers
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
        background:black;
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

def autoDrive () :
  # check distance from obstacles in cm.
  fd = forward_distance()
  print('forward ', fd)
  # then take actions in milli seconds
  if fd < 10 :
     stop(100)
     back(200)
     print ("+Auto Stop back")
  elif fd < 25 :
      stop(100)
      ld=left_distance ()
      rd=right_distance ()
      print('L ',ld, ' R ', rd)

      if ld < 15 and rd < 15 :
        # backward
        back(800)
        left(300)
        print ("+Auto back left")

      elif ld > rd :
        # left
        back(100)
        right(300)
        print ("+Auto left")

      else : # ld <= rd
        # right
        back(100)
        left(300)
        print ("+Auto right")
  else  : # >= 25
    # forward
    forward (100)
    print ("+Auto forward")

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

# main program starts here
print (forward_distance())

stop()

import network

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifissid,wifipass)
count = 7
while not wifi.isconnected() and count > 0 :
    count -= 1
    print ('.')
    time.sleep(1)

if wifi.isconnected() :
    print('network config:', wifi.ifconfig())
    #Setup Socket WebServer
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()


    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(('', 80))
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:80/")
else  :
    print('No Wifi. Auto Mode')
    auto = True


while True:
    if auto :
        autoDrive()
    elif wifi.isconnected()  :
        remoteControl()