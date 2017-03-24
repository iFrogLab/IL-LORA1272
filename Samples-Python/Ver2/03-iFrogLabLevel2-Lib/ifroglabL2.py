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


# python ap12-SendReceive-data.py -u /dev/tty.usbserial-A700eGFx -r 115200 -a T  -s a1,2,3,4,5 -b /dev/tty.ttyAMA0 -m 9600
# python ap12-SendReceive-data.py -u /dev/tty.wchusbserial1410 -r 115200 -a R

import serial
import platform
import ifroglab

from serial import SerialException
import time
import sys
import glob



class LoRaL2(ifroglab.LoRa):   
    lastData=[]
    def __init__(self,GatewayNoode):
        self.mode=GatewayNoode
        #:V  1.找這台機器有幾個LoRa , 設定其中之一為Gateway。
        #: 2.設定default, read 模式，等待Node。
        #. 3.如果有資料進來ack 資料回去。
        #. 4.再繼續等待資料，直接結束。


    def FunLora_init(self,i_portPath):
      super(LoRaL2, self).FunLora_initByName(i_portPath)
      #: 1.找這台機器有幾個LoRa , 設定其中之一為Gateway。
      self.firmwareVersion=0
      self.FunLora_0_GetChipID()                          #讀取F/W版本及Chip ID
      print("firmware Version= %d" % self.firmwareVersion)
      print("deviceID= %d" % self.deviceID)
      if (self.firmwareVersion==0):                       # failed, this port is not a LoRa device
          return False
      print("Init, FunLora_1_Init()")         # 重置 & 初始化
      self.FunLora_1_Init()



    def FunLora_BoardcaseRead(self):
      # 2.設定default, read 模式，等待Node。  
      # 讀取設定狀態
      self.FunLora_2_ReadSetup();
      # 設定讀取和頻段
      self.FunLora_3_RX();
      #讀取資料
      counter=0
      while True:
        data=self.FunLora_6_readPureData();
        if(len(data)>0):
          if(self.Fun_ArrayIsSame(self.lastData,data)==False):
            self.lastData = list(data)
            counter=counter+1   
            print(data)   
            print(counter)







      

    





