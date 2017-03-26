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
"""
範例4:
確認，二個LoRa 可以連續大量的　送　和　收資料資料，並組合顯示
ap-Lib-7-lora-ReadLongString.py
ap-Lib-7-lora-WriteLongString.py
"""

import ifroglab



LoRa = ifroglab.LoRa()
LoRa.TimeStamp()

# 找最後一個USB  UART 設備
print("List All Ports, serial_ports()")
serPorts = LoRa.serial_allPorts()
print(serPorts)
portName = serPorts[-1]

# 打開Port
print("Open Port, FunLora_init()")
ser = LoRa.FunLora_initByName(portName)

# 讀取F/W版本及Chip ID
print("Get Firmware Version, FunLora_0_GetChipID()")
LoRa.FunLora_0_GetChipID()
# 重置 & 初始化
print("Init, FunLora_1_Init()")
LoRa.FunLora_1_Init()
# 讀取設定狀態
print("\n[4]:FunLora_2_ReadSetup");
LoRa.FunLora_2_ReadSetup();

# 設定讀取和頻段
# print("\n[7]:FunLora_3_RX")
LoRa.FunLora_3_RX();
LoRa.TimeStamp()

while True:
    data=LoRa.FunLora_5_readString()
    print data
    LoRa.TimeStamp()
    #print ','.join('{:02x}'.format(x) for x in data)





# 關閉
LoRa.FunLora_close()


"""
import ifroglab
import time


allData=[0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]
lastData=[0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]


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

# 設定讀取和頻段
# print("\n[7]:FunLora_3_RX")




LoRa.debug=False
counter=0

lastData=[]
while True:
  #讀取資料
  #print("\n[8]:FunLora_6_read")
  LoRa.FunLora_3_RX();
  data=LoRa.FunLora_6_read();
  #data=LoRa.FunLora_6_readPureData()
  #if LoRa.Fun_ArrayIsSame(data, lastData)==False:
  #   lastData=LoRa.Fun_ArrayCopy(data)
  #print data
  print(data.encode('hex'))
  #print ','.join('{:02x}'.format(x) for x in data)
  #print(" recive data: %s"% str)
  #print(data)
  time.sleep(0.2)


"""

"""

while True:
  # 讀取資料
  LoRa.FunLora_3_RX();
  #print("\n[8]:FunLora_6_read")
  data=LoRa.FunLora_6_read()
  #print data
  #data=LoRa.FunLora_6_readPureData()
  print data
  if LoRa.Fun_ArrayIsSame(data, lastData)==False:
     lastData=LoRa.Fun_ArrayCopy(data)
     #print("-----------------------------------------------------")
     #print ','.join('{:02x}'.format(x) for x in data)
     #print''.join(chr(i) for i in data)
     #counter=counter+1
     #print("counter")
     #print(" recive data: %s"% data)
     #print(data)
  #time.sleep(1)


"""

# 關閉
LoRa.FunLora_close() 


