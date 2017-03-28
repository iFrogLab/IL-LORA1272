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

import Queue
import threading
import urllib2
import time
#import sys, getopt
#import time
#import numpy
#import RPi.GPIO as GPIO ## Import GPIO library


class LoRa(object):   
    deviceID=0
    deviceIDArray=[]
    waitTillRespnseTime=5
    debug=True
    sleep=0
    firmwareVersion=0
    waitCount=99999
    segLen=16
    lastData = []
    Freq=[0x65,0x6C,0x0f]


    def __init__(self):
        #self.name = name
        #self.number = number
        #self.balance = balance
        self.a1=1



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
       self.deviceIDArray=[]
       if(len(data)>5+3):
          j=0
          for i in range(5,len(data)-1):
             t1=t1+((int(data[i].encode('hex'),16))*num)
             num=num/0xff
             t2=int(data[i].encode('hex'),16)
             self.deviceIDArray.append(t2)
             j=j+1
             #print(data[i].encode('hex'))
             #print(t1)
          self.deviceID=t1;
          if self.deviceID==0:
              print("This port cannot find iFrogLab LoRa device.")
              sys.exit()()
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
       array1=[0xC1,3,5,2,1,self.Freq[0],self.Freq[1],self.Freq[2],0]
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
       t_DataLen=0
       i=0
       if(t_len>6):
          if(data[1].encode('hex')=="86"):
             t_DataLen=ord(data[2])
             if(t_DataLen>2 and t_DataLen<=18):
               for i in range(3,t_DataLen-2+2+1):
                 try:
                     data2.append(ord(data[i]))
                     #if self.debug == True:
                     #   #print ','.join('{:02x}'.format(x) for x in data)
                     #   print hex(data2[i])
                 except:
                     print("except")
                     return None
               if self.debug == True:
                  print ','.join('{:02x}'.format(x) for x in data2)
                  #   print hex(data2[i])
               return data2
       return None



    # 讀取LoRa 是否有新的資料 (　限firmwareVersion>=5 才有的功能)
    def FunLora_7_readCounter(self):
       array1=[0xC1,0x7,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data

    """
    # 讀取LoRa 傳過來的資料
    def FunLora_6_read(self):
       array1=[0xC1,0x6,0x0,0]
       array1[3]=self.Fun_CRC(array1)
       data=self.FunLora_ChipSendByte(array1)
       return data
    """

    # 寫入
    def FunLora_5_write16bytesArrayString(self,data_array):
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
        return data


    # 寫入
    def FunLora_5_write16bytesArray(self,data_array):
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
        #if self.debug==True:
        #   print(data.encode('hex'))
        return data






    def Fun_ArrayCopy(self, A):
        t_len=len(A)
        B=[]
        for i in A:
            B.append(i)
        return B

    def Fun_ArrayToString(self, A):
        t_len = len(A)
        B = ""
        for i in A:
            #B.append(i)
            B=B+str(unichr(i))
        return B

    def Fun_ArrayIsSame(self, A, B):
        q = Queue.Queue()
        t = threading.Thread(target=self.Fun_ArrayIsSame_thread, args=(q, A, B))
        t.daemon = True
        t.start()

        s = q.get()
        return s


    def Fun_ArrayIsSame_thread(self,q, A, B):
        if (len(A) > 0 and len(B) > 0):
            if (len(A) != len(B)):
                q.put(False)
                return False
            else:
                IsSame = True
                i = 0
                for t1 in A:
                    t2 = B[i]
                    if (t1 != t2):
                        q.put(False)
                        return False
                    i = i + 1
                q.put(True)
                return True
        else:
            q.put(False)
            return False  # No data


    counter = 101234567890123




    # 寫入長資料
    def FunLora_5_writeString(self, iString):
        data_array=iString+'\n'
        t_Len = len(data_array)
        t_lenCurrent = 0
        t_seg_len = self.segLen
        t_segments = t_Len / t_seg_len
        if (t_Len % t_seg_len) > 0:  # 處理餘數
            t_segments = t_segments + 1
        for t_segment in range(0, t_segments):
            CMD_Data = []
            for t_x in range(0, t_seg_len):
                #CMD_Data.append(ord(data_array[t_lenCurrent]))
                CMD_Data.append(data_array[t_lenCurrent])
                t_lenCurrent = t_lenCurrent + 1
                if t_lenCurrent >= t_Len:  # 處理餘數
                    break
            print(CMD_Data)
            self.FunLora_3_TX()
            self.FunLora_5_write16bytesArray(CMD_Data);
            #time.sleep(0.005)

    # 寫入長資料
    def FunLora_5_write(self, data_array):
        #data_array=iString+'\n'
        data_array.append(10)
        t_Len = len(data_array)
        t_lenCurrent = 0
        t_seg_len = self.segLen
        t_segments = t_Len / t_seg_len
        if (t_Len % t_seg_len) > 0:  # 處理餘數
            t_segments = t_segments + 1
        for t_segment in range(0, t_segments):
            CMD_Data = []
            for t_x in range(0, t_seg_len):
                #CMD_Data.append(ord(data_array[t_lenCurrent]))
                CMD_Data.append(data_array[t_lenCurrent])
                t_lenCurrent = t_lenCurrent + 1
                if t_lenCurrent >= t_Len:  # 處理餘數
                    break
            # print(CMD_Data)
            self.FunLora_3_TX()
            self.FunLora_5_write16bytesArray(CMD_Data);
            #time.sleep(0.005)



    # 讀 長資料
    def FunLora_5_read_v1(self):
        LoRa.debug = False
        counter = 0
        allData = []
        lastData = []
        while True:
            # 讀取資料
            data = self.FunLora_6_readPureData()
            if self.Fun_ArrayIsSame(data, lastData) == False:
                lastData = self.Fun_ArrayCopy(data)
                #lastData = self.Fun_ArrayToString(data)
                t_len = len(data)
                if t_len >= 1:
                    for i in data:
                        allData.append(i)
                        #allData = allData + lastData
                    if data[t_len - 1] == 10:
                        del data[-1]
                        # print ','.join('{:02x}'.format(x) for x in data)
                        return allData


    def FunLora_6_read(self):
        allData = []
        while True:
            # 讀取資料
            data = self.FunLora_6_readPureData()
            if self.Fun_ArrayIsSame(data, self.lastData) == False:
                self.lastData = self.Fun_ArrayCopy(data)
                t_len = len(data)
                if t_len >= 1:
                    for i in data:
                        allData.append(i)
                    if data[t_len - 1] == 10:
                        return allData


    # 讀 長資料
    def FunLora_5_readString(self):
        LoRa.debug = False
        counter = 0
        allData=""
        lastData = []
        while True:
            # 讀取資料
            data = self.FunLora_6_readPureData()
            if self.Fun_ArrayIsSame(data, lastData) == False:
                #lastData = self.Fun_ArrayCopy(data)
                t_len=len(data)
                if t_len >= 1:
                  lastData = self.Fun_ArrayToString(data)
                  #for i in data:
                  #allData.append(i)
                  allData=allData+lastData
                  if  data[t_len-1]==10:
                     del data[-1]
                     #print ','.join('{:02x}'.format(x) for x in data)
                     return allData



    lastTime=0
    def TimeStamp(self):
        ts = time.time()
        print "Time Stamp:%s" %(ts- self.lastTime)
        self.lastTime=ts




    # 寫入長資料
    def FunLora_10_write_AndCheckKey(self, data_array):
      #data_array=iString+'\n'
      t_Len2=len(data_array)
      if t_Len2>253:
        print("error 3: data cannot biger then 253 bytes")
      else:
        data_array.insert(0, t_Len2)
        data_array.append(10)
        t_Len = len(data_array)
        t_lenCurrent = 0
        t_seg_len = self.segLen
        t_segments = t_Len / t_seg_len
        if (t_Len % t_seg_len) > 0:  # 處理餘數
            t_segments = t_segments + 1
        for t_segment in range(0, t_segments):
            CMD_Data = []
            for t_x in range(0, t_seg_len):
                #CMD_Data.append(ord(data_array[t_lenCurrent]))
                CMD_Data.append(data_array[t_lenCurrent])
                t_lenCurrent = t_lenCurrent + 1
                if t_lenCurrent >= t_Len:  # 處理餘數
                    break
            print(CMD_Data)
            self.FunLora_3_TX()
            self.FunLora_5_write16bytesArray(CMD_Data);
            #time.sleep(0.005)

    def FunLora_10_read_AndCheckKey(self):
          allData = []
          ts = time.time()
          while True:
              # 讀取資料
              self.FunLora_3_RX();
              data = self.FunLora_6_readPureData()
              if data!=None:
                  t_len = len(data)
                  if t_len >= 1:
                      #if self.Fun_ArrayIsSame(data, self.lastData) == False:
                      self.lastData = self.Fun_ArrayCopy(data)
                      if t_len >= 1:
                         for i in data:
                            allData.append(i)
                         t1=len(allData)-2
                         t2=allData[0]
                         if allData[t_len - 1] == 10 and allData[0]==t1:
                            # del allData[0]
                            #del allData[-1]
                            allData2 = []
                            for i in range(1,len(allData)-1):
                                allData2.append(allData[i])
                            return allData2
                         else:
                             if(len(allData)>256):
                               allData = []
                             ts2 = time.time()
                             if(ts2-ts>2):
                               allData = []
                      ts3 = time.time()
                      if (ts2 - ts > 4):
                         return None


