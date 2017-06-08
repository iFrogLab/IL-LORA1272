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


# 設定讀取和頻段
print("\n[7]:FunLora_3_RX")
LoRa.FunLora_3_RX();




#讀取資料
print("\n[8]:FunLora_5_write")
data=LoRa.FunLora_6_read();

i=0	
for t1 in data:
   print("data[%d]= %s"%(i,t1))
   i=i+1


#讀取資料
print("\n[9]:FunLora_7_readCounter")
data=LoRa.FunLora_7_readCounter()

#i=0	
#for t1 in data:
#   print("data[%d]=%s,  Hex->%s"%(i,t1,t1.encode('hex')))
#   i=i+1

#print("data[4]=%s,  Hex->%s"%(data[4],data[4].encode('hex')))
#print("data[5]=%s,  Hex->%s"%(data[5],data[5].encode('hex')))

#讀取資料
counter=0
lastData=[]
LoRa.debug=False
while True:
    data=LoRa.FunLora_6_readPureData()#取得收到的純資料
    if(len(data)>0):
        if(LoRa.Fun_ArrayIsSame(lastData,data)==False):  #  僅顯示出不同的資料
            lastData = list(data)
            counter=counter+1   
            print(data)   
            print(counter)







# 關閉
LoRa.FunLora_close() 
ser.close()

