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

from serial import SerialException
import time
import sys
import glob



#import sys, getopt
#import time
#import numpy
#import RPi.GPIO as GPIO ## Import GPIO library


class LoRa(object):   
    deviceID=0
    waitTillRespnseTime=5
    debug=True
    sleep=0
    firmwareVersion=0
    waitCount=99999

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
        return 'Account({0}, {1}, {2})'.format(self.name, self.number, self.balance)/Users/powenko/Desktop/powenko/github/IL-LORA1272/Samples-Python/Ver2/ifroglab.py
    


    def serial_allPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                #s = serial.Serial(port)
                #s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass           
        return result


    # 計算CRC 檢查碼   
    def Fun_CRC(self,data):
       crc=0
       for i in data:
         crc=crc^i
       return crc

    def serial_ports(self):
      if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
      elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
      elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
      else:
        raise EnvironmentError('Unsupported platform')
      result = []
      for port in ports:
        try:
            if port=="/dev/tty.Bluetooth-Incoming-Port":
              s=1
            else:
              s = serial.Serial(port)
              s.close()
              result.append(port)
        except (OSError, serial.SerialException):
            pass
      return result

    # open Serial Port   


    def FunLora_init(self):
      try:
        self.portPath=self.Fun_OS()
        print(self.portPath)
        self.ser = serial.Serial(self.portPath, 115200, timeout=3)    
        return self.ser
      except SerialException:
        print("port already open")

    # open Serial Port  by  name , like "/dev/xxx"
    def FunLora_initByName(self,i_portPath):
      try:
        print(i_portPath)
        self.ser = serial.Serial(i_portPath, 115200, timeout=3)    
        return self.ser
      except SerialException:
        print("port already open")

    #  get all USB Uart Port.
    def Fun_OS(self):
      OSVersion=platform.system()
      self.port_path="/dev/cu.usbserial"
      print OSVersion
      if OSVersion=="Darwin":              #MAC Port
         #self.port_path="/dev/cu.usbserial"
         #self.port_path="/dev/cu.usbmodem1421"
         self.port_path="/dev/cu.usbserial-A700eGFx"
      elif OSVersion=="Linux":            #Linux Port
         self.port_path="/dev/ttyUSB0"
      self.ports=self.serial_ports()
      print(self.ports)
      t1=len(self.ports)
      print("This device has %d Serial devices"%t1)
      for self.port_path in self.ports:
        #if t1>0:
        #self.port_path=self.ports[0]
        #self.ser=self.port_path
        # 判對是否是LoRa 接在上面
        print("1")
        self.ser=self.FunLora_initByName(self.port_path)
        print(self.ser)
        data=self.FunLora_0_GetChipID()
        print(data)
        if(len(data)>1):
          return self.port_path  
      return self.port_path

    # 送byte 到　Chip 上
    def FunLora_ChipSendByte(self,array1):    
      try:
        if self.debug==True:
            #print array1
            print ''.join('{:02x}'.format(x) for x in array1)
        self.ser.write(serial.to_bytes(array1))
        time.sleep(0.04)
        bytesToRead = self.ser.inWaiting()
        i=0
        while True:
           data = self.ser.read(bytesToRead)
           i=i+1
           if len(data)>0 or i>self.waitCount:
               break
        if self.debug==True:
            print(data.encode('hex'))
      except (OSError, serial.SerialException):
        pass
      return data

    def Fun_ser_Write(self,array1):
      try:
         self.ser.write(serial.to_bytes(array1))
      except SerialException:
        print("Fun_ser_Write error")


    # close Serial Port
    def FunLora_close(self):
      try:
        self.ser.close()
      except SerialException:
        print("port already open")
    


    def FunLora_0_GetChipID(self):
       array1=[0x80,0x00,0x00,0]
       array1[3]=self.Fun_CRC(array1)
       if self.debug==True:
          print array1
       self.Fun_ser_Write(array1)
       time.sleep(0.01)
       bytesToRead = self.ser.inWaiting()
       data = self.ser.read(bytesToRead)
       if self.debug==True:
          print(data.encode('hex'))
       # get Device ID // deviceID
       t1=0
       num=0xffffff;
       if(len(data)>5):
          for i in range(5,len(data)-1):
            #print(num)
            t1=t1+((int(data[i].encode('hex'),16))*num)
            num=num/0xff;    
            #print(data[i].encode('hex'))
            #print(t1)
          self.deviceID=t1; 
          #get Chip ID // firmwareVersion
          self.firmwareVersion=int(data[4].encode('hex'),16)
       return data

    # 4 bytes 組合為ID　
    def FunLora_0_GetDeviceID(self):
       array1=[0x80,0x00,0x00,0] 
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1) 
       t1=0
       num=0xffffff;
       for i in range(5,len(data)-1):
          #print(num)
          t1=t1+((int(data[i].encode('hex'),16))*num);
          num=num/0xff;    
          #print(data[i].encode('hex'))
          #print(t1)
       self.an_id=t1;    
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

    # 設定讀取和頻段
    def FunLora_3_RX(self):
       array1=[0xC1,3,5,3,1,0x65,0x6C,0x0f,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 設定寫入和頻段
    def FunLora_3_TX(self):
       array1=[0xC1,3,5,2,1,0x65,0x6C,0x0f,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data




        # 讀取LoRa 傳過來的資料去掉CRC, RSSI 等別的資料
    def FunLora_6_readPureData(self):
       array1=[0xC1,0x6,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       data2=[]
       t_len=len(data)
       i=0
       if(t_len>6):
          for i3 in data:
            if(i>=3):
              data2.append(ord(i3))
              if (i>t_len-5):
                break
            i=i+1    
       if self.debug==True:     
           print(data2)   
       return data2   



    # 讀取LoRa 是否有新的資料 (　限firmwareVersion>=5 才有的功能)
    def FunLora_7_readCounter(self):
       array1=[0xC1,0x7,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 讀取LoRa 傳過來的資料
    def FunLora_6_read(self):
       array1=[0xC1,0x6,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data
    # 寫入
    
    def FunLora_5_write16bytesArray(self,data_array):
        TX_Data=data_array
        ##[0x01,0x02,0x03]
        CMD_Data=[0xc1,0x05]
        CMD_Data.append(len(TX_Data))
        for i3 in data_array:
           CMD_Data.append(ord(i3))
        CRC=self.Fun_CRC(CMD_Data)
        CMD_Data.append(CRC)
        while True:
          data=self.FunLora_ChipSendByte(CMD_Data)
          time.sleep(self.sleep)
          if len(data)!=6:                            # 確認回傳的是　c1aa01553f
            break
        if self.debug==True:
           print(data.encode('hex'))    
        return data


    # 寫入
    def FunLora_5_write16bytes(self,data_array):
        TX_Data=data_array
        ##[0x01,0x02,0x03]
        CMD_Data=[0xc1,0x05]
        CMD_Data.append(len(TX_Data))
        for i3 in data_array:
           CMD_Data.append(i3)
        CRC=self.Fun_CRC(CMD_Data)
        CMD_Data.append(CRC)
        while True:
          data=self.FunLora_ChipSendByte(CMD_Data)
          time.sleep(self.sleep)
          if len(data)!=6:                            # 確認回傳的是　c1aa01553f
            break
        if self.debug==True:
           print(data.encode('hex'))    
        return data

    # 寫入
    def FunLora_5_writeString(self,data_array):
        #TX_Data=data_array
        t_Len=len(data_array)
        t_lenCurrent=0
        t_seg_len=14
        t_segments=t_Len/t_seg_len
        if (t_Len%t_seg_len)>0:                               #處理餘數
          t_segments=t_segments+1
        for t_segment in range(0, t_segments):
            CMD_Data=[]
            for t_x in range(0, t_seg_len):
                CMD_Data.append(ord(data_array[t_lenCurrent]))
                t_lenCurrent=t_lenCurrent+1
                if t_lenCurrent >= t_Len:                     #處理餘數
                   break
            print(CMD_Data)
            self.FunLora_5_write16bytes(CMD_Data)


    # 寫入並等待對方回應
    # def FunLora_5_writeStringWaitTillResponse(self,data_array):





    def Fun_ArrayIsSame(self,A,B):
        if(len(A)>0 and len(B)>0 ):
          if(len(A)!=len(B)):
            return True
          else:
            IsSame=True
            i=0
            for t1 in A:
              t2=B[i]
              #print("data[%d]=%s,  Hex->%s"%(i,t1,t1.encode('hex')))
              #print("data[%d]=%s,  Hex->%s"%(i,t2,t2.encode('hex')))
              if(t1!=t2):
                return False
              i=i+1    
            return True  
        else:
           return False   # No data  










