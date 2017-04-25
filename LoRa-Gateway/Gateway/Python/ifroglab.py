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
        return 'Account({0}, {1}, {2})'.format(self.name, self.number, self.balance)/Users/powenko/Desktop/powenko/github/IL-LORA1272/Samples-Python/Ver2/ifroglab.py
    


    def serial_allPorts(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
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
                s = serial.Serial(port)
                s.close()
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
      """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
      """
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
        #self.portPath=self.Fun_OS()
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


    def FunArrayDel(self,array1,index): 
        t1=len(array1)
        array2=[]
        j=0
        for i in range(t1):
          if not index==i:
            #print(i)
            array2.append(array1[i])
            #j=j+1 
        return array2

    def FunArrayToHexString_v2(self,array1):
        #urlData = "/AjaxIoT.php?action=insertByAPIKey&KeyName=%s&Data=%d&Datatype=1&APIKey=iloveifroglab" % (t1, x1);
        t1=len(array1)
        str2=" "
        for i in range(t1-1):
            #print("array1[%s]=%s,  Hex->%s" % (i, array1[i], array1[i].encode('hex')))
            x1 = (int(array1[i].encode('hex'), 16))
            x2=str( array1[i].encode('hex'))
            str2=str2+x2
        return str2
        #return array1.encode('hex')



    def FunArrayToHexStringKeepPureData(self,array1):    
        array2=array1
        print("FunArrayToHexStringKeepPureData")
        str1=array1.encode('hex')
        print(str1)        
        t1=len(array1)
        array2=self.FunArrayDel(array2,t1)
        array2=self.FunArrayDel(array2,2)
        array2=self.FunArrayDel(array2,1)
        array2=self.FunArrayDel(array2,0)
        str2=self.FunArrayToHexString_v2(array2)
        print(str2)
        return str2

    def FunArrayToHexString(self,array1):    
      try:    
        str1=array1.encode('hex')
        print(str1)
      except (OSError, serial.SerialException):
        pass
      return str1

    # 送byte 到　Chip 上
    def FunLora_ChipSendByte(self,array1):    
      try:
        print array1
        self.ser.write(serial.to_bytes(array1))
        time.sleep(0.02)
        bytesToRead = self.ser.inWaiting()
        data = self.ser.read(bytesToRead)
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
       print array1
       self.Fun_ser_Write(array1)
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

    def FunLoRa_FloatTo3Bytes(self,frequency):
      array3=[0x01,0x65,0x6c]
      #if(frequency!=915.00):
      t0=frequency*100
      t1=int(t0)
      #print t1
      #print format(t1, '02x') #16760
      ta1=t1/(0x10000)
      array3[0]=ta1
      print ta1
      ta2=t1-((0x10000)*ta1)
      ta2=ta2/(0x100)
      array3[1]=ta2
      #print ta2
      print format(ta2, '02x')
      ta3=t1-((0x10000)*ta1)-(ta2*(0x100))
      array3[2]=ta3
      #print array3[2]
      print format(ta3, '02x')
      return array3
        

    # 設定讀取和頻段
    def FunLora_3_RX(self):
       array1=[0xC1,3,5,3,1,0x65,0x6C,0xf,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 設定讀取和頻段
    def FunLora_3_RX2(self,frequency):
       array2=self.FunLoRa_FloatTo3Bytes(frequency)
       array1=[0xC1,3,5,3,array2[0],array2[1],array2[2],0xf,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 讀取LoRa 傳過來的資料
    def FunLora_6_read(self):
       array1=[0xC1,0x6,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 設定寫入和頻段
    def FunLora_3_TX(self):
       array1=[0xC1,3,5,2,array2[0],array2[1],array2[2],0xf,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    # 設定寫入和頻段
    def FunLora_3_TX2(self,frequency):
       array2=self.FunLoRa_FloatTo3Bytes(frequency)
       array1=[0xC1,3,5,2,1,0x65,0x6C,0xf,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data   

    # 寫入測試
    def FunLora_5_write_test(self):
       array1=[0xC1,0x5,0x5,0x61,0x62,0x63,0x64,0x65,0]
       array1[8]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    def FunLora_5_write16bytesArray(self,data_array):
        #self.ser.write(serial.to_bytes([0xc1,0x03,0x05,0x02,0xe4,0xc0,0x00,0x03]))
        #data = ser.read(5)
        #print data.encode('hex')
        TX_Data=data_array
        ##[0x01,0x02,0x03]
        CMD_Data=[0xc1,0x05]
        CMD_Data.append(len(TX_Data))
        for i3 in data_array:
           #CMD_Data.append(int(i3, 16))
           CMD_Data.append(ord(i3))
        ##ser.write(serial.to_bytes([0xc1,0x05,0x03,0x01,0x02,0x03]))
        CRC=self.Fun_CRC(CMD_Data)
        CMD_Data.append(CRC)
        print(CMD_Data)
        data=self.FunLora_ChipSendByte(CMD_Data)
        return data

        ##ser.write(serial.to_bytes(TX_Data))
        #ser.write(CMD_Data)
        #
        #print ("Send:")
        ##print ','.join(format(x, '02x') for x in serial.to_bytes(TX_Data))
        #print ','.join([i2 for i2 in TX_Data])
        #data = ser.read(5)
        #print data.encode('hex')

    # 讀取LoRa 傳過來的資料
    def FunLora_7_readCounter(self):
       array1=[0xC1,0x7,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data








