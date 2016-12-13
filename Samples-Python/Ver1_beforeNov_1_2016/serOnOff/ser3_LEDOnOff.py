#!/usr/bin/env python
# author: Powen Ko
import serial
import time

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv
        

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)


while True:
    rcv = readlineCR(port)
    print(rcv)   
    port.write(rcv)
