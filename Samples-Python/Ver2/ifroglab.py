# coding=UTF-8
# -*- coding: utf8 -*-
# * iFrogLab IL-LORA1272  www.ifroglab.com
# *
# * 功能,             USB to TTL , IFROGLAB LORA 
# * 電源VDD,          3.3V       ,Pin 3         
# * 接地GND,          GND        ,Pin 1        
# * 接收反應Host_IRQ,  null       , Pin 2        
# * UART,             RX         ,UART_RX  Pin 7 
# * UART,             TX         ,UART_TX  Pin 8 


# python ap12-SendReceive-data.py -u /dev/tty.usbserial-A700eGFx -r 115200 -a T  -s a1,2,3,4,5 -b /dev/tty.ttyAMA0 -m 9600
# python ap12-SendReceive-data.py -u /dev/tty.wchusbserial1410 -r 115200 -a R

import serial
import platform

from serial import SerialException
import time
#import sys, getopt
#import time
#import numpy
#import RPi.GPIO as GPIO ## Import GPIO library


class LoRa:
    def __init__(self):
        #self.name = name
        #self.number = number
        #self.balance = balance
        self.a1=1
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('amount must be positive')
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise RuntimeError('balance not enough')
        self.balance -= amount
    
    def __str__(self):
        return 'Account({0}, {1}, {2})'.format(self.name, self.number, self.balance)
       
    # 計算CRC 檢查碼   
    def Fun_CRC(self,data):
       crc=0
       for i in data:
         crc=crc^i
       return crc

    def Fun_OS(self):
       OSVersion=platform.system()
       self.port_path="/dev/cu.usbserial"
       print OSVersion
       if OSVersion=="Darwin":              #MAC Port
         self.port_path="/dev/cu.usbserial"
       elif OSVersion=="Linux":            #Linux Port
         self.port_path="/dev/ttyUSB0"
       return self.port_path

    # 送byte 到　Chip 上
    def FunLora_ChipSendByte(self,array1):    
       print array1
       self.ser.write(serial.to_bytes(array1))
       time.sleep(0.04)
       bytesToRead = self.ser.inWaiting()
       data = self.ser.read(bytesToRead)
       print(data.encode('hex'))
       return data


    def FunLora_close(self):
      try:
        self.ser.close()
      except SerialException:
        print("port already open")
       
       

    def FunLora_init(self):
      try:
        self.portPath=self.Fun_OS()
        print(self.portPath)
        self.ser = serial.Serial(self.portPath, 115200, timeout=3)    
        return self.ser
      except SerialException:
        print("port already open")

    def FunLora_0_GetChipID(self):
       array1=[0x80,0x00,0x00,0]
       array1[3]=self.Fun_CRC(array1)
       print array1
       self.ser.write(serial.to_bytes(array1))
       time.sleep(0.01)
       bytesToRead = self.ser.inWaiting()
       data = self.ser.read(bytesToRead)
       print(data.encode('hex'))
       return data

    # 重置 & 初始化
    def FunLora_1_Init(self):
       array1=[0xc1,0x01,0x00,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 讀取設定狀態
    def FunLora_2_ReadSetup(self):
       array1=[0xc1,0x02,0x00,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 設定寫入和頻段
    def FunLora_3_TX(self):
       array1=[0xC1,3,5,2,1,0x65,0x6C,0x3,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 寫入測試
    def FunLora_5_write_test(self):
       array1=[0xC1,0x5,0x5,0x61,0x62,0x63,0x64,0x65,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 設定讀取和頻段
    def FunLora_3_RX(self):
       array1=[0xC1,3,5,3,1,0x65,0x6C,0x3,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 讀取LoRa 傳過來的資料
    def FunLora_6_read(self):
       array1=[0xC1,0x6,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data













