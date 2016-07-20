#!/usr/bin/env python
# author: Powen Ko
import serial
import time
import RPi.GPIO as GPIO

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv
        
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)
port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
portbt = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)


while True:
    rcv = readlineCR(port)
    print(rcv)   
    port.write(rcv)
    portbt.write(rcv)
    str1=rcv.find("h")
    if str1 >= 0 :
        GPIO.output(4,1)
    str1=rcv.find("l")   
    if str1 >= 0 :
        GPIO.output(4,0)
    time.sleep(0.1)
