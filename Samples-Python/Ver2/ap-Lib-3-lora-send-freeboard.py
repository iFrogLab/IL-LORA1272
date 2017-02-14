# www.ifroglab.com
# -*- coding: utf8 -*-
# coding=UTF-8
# * iFrogLab IL-LORA1272  www.ifroglab.com
# *
# * 功能,             USB to TTL , IFROGLAB LORA
# * 電源VDD,          3.3V       ,Pin 3
# * 接地GND,          GND        ,Pin 1
# * 接收反應Host_IRQ,  null       , Pin 2
# * UART,             RX         ,UART_RX  Pin 7
# * UART,             TX         ,UART_TX  Pin 8


import ifroglab
import time
import serial

def Fun_CRC(data):
    crc=0
    for i in data:
        crc=crc^i
    return crc

LoRa = ifroglab.LoRa()

# 找最後一個USB  UART 設備
print("List All Ports, serial_ports()")
serPorts=LoRa.serial_allPorts()
print(serPorts)
portName=serPorts[-1]



# 打開Port
print("Open Port, FunLora_init()")
ser=LoRa.FunLora_initByName(portName)


#讀取F/W版本及Chip ID
print("Get Firmware Version, FunLora_0_GetChipID()")
LoRa.FunLora_0_GetChipID()

# 重置 & 初始化
print("Init, FunLora_1_Init()")
LoRa.FunLora_1_Init()


# 讀取設定狀態
print("\n[4]:FunLora_2_ReadSetup");
LoRa.FunLora_2_ReadSetup();


# 設定寫入和頻段
print("\n[7]:FunLora_3_TX")
LoRa.FunLora_3_TX();


#寫入資料
print("\n[8]:FunLora_5_write")
LoRa.FunLora_5_write_test();

#寫入資料
print("\n[10]:FunLora_5_write16bytesArray")
LoRa.FunLora_5_write16bytesArray("abcdefghijklmnop");



"""

#!/usr/bin/env python

import serial

import time

import requests

import datetime

import picamera

import os

import sys

import logging

camera = picamera.PiCamera()

camera.stop_preview() #close camera preview window

ARCHIVE_DATA_PERIOD=30  #Period (minutes) time length for history data

PERIODLY_PHOTO_TAKE=5  #Period (minutes) time length for taking a picture

DEBUG_DISPLAY=0  #Will display the log message?

AMAZON_HOST_URL=’http://ec2-52-33-24-149.us-west-2.compute.amazonaws.com/room/&#8217;

AMAZON_SSH_STRING=’ec2-user@ec2-52-33-24-149.us-west-2.compute.amazonaws.com:/var/www/html/room/’

lastPeopleDetectSeconds=0;

def debugPrint(dataDisplay):

if DEBUG_DISPLAY==1:

print dataDisplay

def readlineCR(port):

rv = “"

while True:

ch = port.read()

rv += ch

if ch==’\r’ or ch==":

return rv.strip()

def submitDweet(typeSubmit,dataSubmit):

url = “https://dweet.io/dweet/for/"+typeSubmit

r = requests.get(url, params=dataSubmit)

def submitPhotoToCloud(typeSubmit):

timeString = time.strftime(‘%Y-%m-%d_%H_%M_%S’, time.localtime(time.time()))

timeDisplay = time.strftime(‘%Y/%m/%d %H:%M:%S’, time.localtime(time.time()))

imgname = timeString + ‘.jpg’

camera.capture(‘/data/log/’+imgname)

time.sleep(6)

os.system(‘scp -i /home/pi/raspberry.pem /data/log/’+imgname+’ ‘+AMAZON_SSH_STRING)

payload = { ‘imgurl’:AMAZON_HOST_URL + imgname, ‘datetime’: timeDisplay }

debugPrint(“——————————–“)

debugPrint(“Type —–> “+typeSubmit)

debugPrint(“imgurl —–> “+AMAZON_HOST_URL + imgname)

debugPrint(“datetime —> “+timeDisplay)

debugPrint(“——————————–“)

submitDweet(typeSubmit, payload)

def submitDataToCloud(dataArray):

nowMinutes = int(time.strftime(“%M"))

timeString = time.strftime(‘%Y-%m-%d_%H_%M_%S’, time.localtime(time.time()))

timeDisplay = time.strftime(‘%Y/%m/%d %H:%M:%S’, time.localtime(time.time()))

typeSubmit = “sunplusit-" + dataArray[0:3]

typeSubmit_archive = typeSubmit + “_arch"

debugPrint(“TEST:")

debugPrint(dataArray[4:len(rcv)])

valueCollected = int(dataArray[4:len(rcv)])

imgname="

if dataArray[0]==’P’ and valueCollected==1 and (time.time()-lastPeopleDetectSeconds>180
imgname = ‘P_’ + timeString + ‘.jpg’

camera.capture(‘/data/log/’+imgname)

lastPeopleDetectSeconds = time.time()

debugPrint("    –> Find a man! captured and uploaded a picture of room: " + imgname)

time.sleep(6)

os.system(‘scp -i /home/pi/raspberry.pem /data/log/’+imgname+’ ‘+AMAZON_SSH_STRING )

if dataArray[0]==’W’:

valueCollected = 100 – (int(valueCollected/999) * 100)

payload = {‘v’:valueCollected, ‘datetime’: timeDisplay, ‘imgurl’: AMAZON_HOST_URL + imgname}

debugPrint(“——————————–“)

print(dataArray)

debugPrint(“Length —> “+str(len(dataArray)))

debugPrint(“Type —–> “+typeSubmit)

debugPrint(“Datetime —–> “+timeDisplay)

debugPrint(“v —> “+str(valueCollected))

submitDweet(typeSubmit, payload)

if nowMinutes%ARCHIVE_DATA_PERIOD==0:

debugPrint(“Type —–> “+typeSubmit_archive)

submitDweet(typeSubmit_archive, payload)

debugPrint(“——————————–“)

port = serial.Serial(“/dev/ttyAMA0″, baudrate=9600, timeout=5)

lastPIRAlarmPhoto = 0  #The time for the last PIR alarm and picture

lastPeriodPhoto = 0  #The time for the last picture periodly

while True:

try:

TimeNow = time.time()

TimeNowMinutes = int(time.strftime(“%M"))

#Periodly taking a picture

if TimeNowMinutes%PERIODLY_PHOTO_TAKE==0 and lastPeriodPhoto!=TimeNowMinutes:

lastPeriodPhoto = TimeNowMinutes

submitPhotoToCloud(“sunplusit-roomimg")

#Read data from Serial port

rcv = readlineCR(port)

debugPrint(“Read from serial: " + rcv)

#If there is data from serial port

if len(rcv)>0:

submitDataToCloud(rcv)

sys.stdout.flush()

except:

print “Unexpected error:", sys.exc_info()[0]

sys.stdout.flush()

pass

continue
"""


# 關閉
LoRa.FunLora_close() 
ser.close()

