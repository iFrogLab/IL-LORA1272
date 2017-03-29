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
import datetime


class LoRaL2(ifroglab.LoRa):
    IDnodes=[]
    IDServer = []
    IDNodeIndex=0
    lastData=[]
    debugL2=True
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
        print("This port cannot find iFrogLab LoRa device.")
        self.FunLora_close()
        sys.exit()
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
        #data=self.FunLora_6_readPureData()
        time.sleep(0.1)
        data=self.FunLora_6_read()
        if(len(data)>0):
          if(self.Fun_ArrayIsSame(self.lastData,data)==False):
            self.lastData = list(data)
            counter=counter+1
            if self.debugL2==True:
              print(counter)
              print(data)
              #print ','.join('{:02x}'.format(x) for x in data)



    # [ ] ​Step 1: 啟動時
    #    　　　Node 先透過廣播的方法，把自己的4個bytes 的ID對外宣布，透過　default 頻段，發出廣播，並傳出是node 1 還是gateway 0,
    #    　　　例如:  Node-> broadcast : 0x71, 01, node=0,    ID, ActionID=1,
    #.                                  0x71, 01, node=00,  Node ID3,   Node ID2,   Node ID1,   Node ID0, ActionID=1 CRC
    def LoRaL2_Node_01_FindGateway(self):
      array1 = [0x71, 0x01, 0, 0, 0, 0, 0, 1]
      if (self.deviceID > 0):
        for i in range(0, 4):
          array1[i + 3] = self.deviceIDArray[i]
      #ts1 = time.time()
      while True:
        data=self.LoRaL2_BoardCase_Send(array1,True, 10,True)   #傳送資料，並等帶回傳資料，沒有的話再傳一次
        if(len(data)>0):   # 判是否是正確得資料
          # gatway broadcast->Node   0x72, 01, 1, Gateway ID[0~3], Freq[2], Freq[1], Freq[0], CRC
          if(data[0]==0x72 and data[1]==0x1 and data[2]==0x1 ):   # and data[1]==1 and data[2]==1):
             print("Get Gateway ID~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
             self.IDServer=[]
             self.IDServer.append(data[3])
             self.IDServer.append(data[4])
             self.IDServer.append(data[5])
             self.IDServer.append(data[6])
             self.IDNodeIndex=data[7]
             print("IDNodeIndex= %s" % str(self.IDNodeIndex))
             print("Server ID=  " )
             print ':'.join('{:02x}'.format(x) for x in self.IDServer)

             self.FunLora_close()
             sys.exit()
        #ts2 = time.time()                                       #再發出一次訊號
        print("Message 1: Time out 10 Sec, cannot find Gateway, please make sure gateway is around this device.")




    def LoRaL2_BoardCase_Send(self,i_array,WaitforResponse,waitingTime,CheckIsSame):
      self.debug=False
      # 讀取設定狀態
      #print("\n[4]:FunLora_2_ReadSetup");
      #self.FunLora_1_Init()
      array1 = i_array[:]
      counter = 0
      ts1 = time.time()
      while True:
        self.FunLora_2_ReadSetup();
        self.FunLora_3_TX();
        result=self.FunLora_10_write_AndCheckKey(array1);
        counter = counter + 1
        counter2 = 0
        ts2 = time.time()
        if WaitforResponse==False:        # 不用等　回傳的資料
          return
        else:                             # 是否需要等待有回傳的資料
          time.sleep(0.1)
          while True:
            print(counter)
            self.FunLora_2_ReadSetup();
            self.FunLora_3_RX();
            data = self.LoRaL2_BoardCase_Receive()
            ts3 = time.time()
            counter2 = counter2 + 1
            if (data != None):
              if CheckIsSame==True:
                 if (self.Fun_ArrayIsSame(i_array, data) == False):
                   return data
              else:
                 return data
            if(ts3-ts2>1):                                          #再發出一次訊號
              break
              return None
            time.sleep(0.05)



    def LoRaL2_BoardCase_Receive(self):
      # 讀取設定狀態
      self.FunLora_2_ReadSetup();
      self.FunLora_3_RX();
      ts = time.time()
      if self.debugL2==True:
        print "Time Stamp:%s" % (ts - self.lastTime)
      self.lastTime = ts
      while True:
         allData = self.FunLora_10_read_AndCheckKey()
         if allData!=None and (len(allData)>0):
           return  allData
         if(ts - time.time()>1):
           print("no data")
           return None




    def LoRaL2_GateWay_01_FineNode(self):
      self.debug=False
      self.debugL2=False
      #print("\n[4]:FunLora_2_ReadSetup");
      self.FunLora_2_ReadSetup();
      # 設定讀取和頻段
      self.FunLora_3_RX();
      while True:
        allData = self.FunLora_10_read_AndCheckKey()
        #checkArray=[[]]
        if allData==None or len(allData)==0:
          print("No new Data")
        elif  len(allData)>=2:
          if(self.LoRaL2_GateWay_02_Process71_01(allData)==True):
            print("Get an new Node.")
            #m_nodesObj=['foo', {'bar': ('baz', None, 1.0, 2)}]
            #print(m_nodeObj)
            time.sleep(2)






    # gatway broadcast->Node   0x72, 01, Gateway ID[0~3],Node ID[0~3], Freq[2], Freq[1], Freq[0]
    # gatway broadcast->Node   0x72, 01, Gateway ID[0~3],Node ID index[0], Freq[2], Freq[1], Freq[0]
    def LoRaL2_GateWay_02_Process71_01(self,allData):
       if allData[0] == 0x71 and allData[1] == 0x01 and allData[2] == 0x00:
         print("Message 2: a new Node want to join to Geteway.")
         NodeID=[]
         NodeIDNumer=0
         #array1 = [0x72, 0x01, 1, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0]
         array1 = [0x72, 0x01, 1, 0, 0, 0, 0, 0, 0, 0, 0]
         if (self.deviceID > 0):
           for i in range(0, 4):  # setup Gateway ID
             array1[i + 3] = self.deviceIDArray[i]
           for i in range(0, 4):  # add Node ID
             #array1[i + 3+4] = allData[i+3]
             NodeID.append(allData[i+3])
             #if self.debugL2 == True:
           print ':'.join('{:02x}'.format(x) for x in NodeID)
           array1[ 3 + 4+ 1+0]  =  self.Freq[0]    # Freq
           array1[ 3 + 4+ 1+1]  =  self.Freq[1]    # Freq
           array1[ 3 + 4+ 1+2]  =  self.Freq[2]    # Freq
           if(len(self.IDnodes)==0):
              self.IDnodes.append(self.deviceIDArray)   #加上Server
           j=0
           isFind=False
           for i in self.IDnodes:  # add Node ID
               if (self.Fun_ArrayIsSame(NodeID, i) == True):
                 isFind=True
                 break
               j=j+1
           if(isFind==True):
               array1[0 + 3 + 4] = j
           else:
               self.IDnodes.append(NodeID)      # 加上Node
               array1[0 + 3 + 4] = j
         for i in range(0,5):
           data = self.LoRaL2_BoardCase_Send(array1, False,0,False)  # 傳送資料，並等帶回傳資料，沒有的話再傳一次
           time.sleep(0.08)
         return NodeIDNumer
       else:
         if self.debugL2==True:
            print ','.join('{:02x}'.format(x) for x in allData)
         return None







      

    





