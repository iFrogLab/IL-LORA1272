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



import ifroglabL2
import time
import serial

#: 1.找這台機器有幾個LoRa , 設定其中之一為Gateway。
#: 2.設定default, read 模式，等待Node。
#. 3.如果有資料進來ack 資料回去。
#. 4.再繼續等待資料，直接結束。



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





#######
LoRa2 = ifroglab.LoRa()


# 找最後一個USB  UART 設備
print("List All Ports, serial_ports()")
serPorts=LoRa2.serial_allPorts()
print(serPorts)
portName=serPorts[-2]



# 打開Port
print("Open Port, FunLora_init()")
ser=LoRa2.FunLora_initByName(portName)


#讀取F/W版本及Chip ID
print("Get Firmware Version, FunLora_0_GetChipID()")
LoRa2.FunLora_0_GetChipID()



# 重置 & 初始化
print("Init, FunLora_1_Init()")
LoRa2.FunLora_1_Init()
# 讀取設定狀態
print("\n[4]:FunLora_2_ReadSetup");
LoRa2.FunLora_2_ReadSetup();


counter=0
while True:
  # 設定寫入和頻段
  #print("\n[7]:FunLora_3_TX")
  LoRa2.FunLora_3_TX();
  # 寫入資料
  #print("\n[10]:FunLora_5_write16bytesArray")
  LoRa2.FunLora_5_write16bytesArray(str(counter));
  counter=counter+1
  print(counter)
  time.sleep(0.01)

# 關閉
LoRa2.FunLora_close()






"""


LoRa = ifroglabL2.LoRaL2("node")

# 找最後一個USB  UART 設備
print("List All Ports, serial_ports()")
serPorts=LoRa.serial_allPorts()
print(serPorts)
portName=serPorts[-2]

# 打開Port
print("Open Port, FunLora_init()")
if(LoRa.FunLora_init(portName)==False):
	print("error code 1:cannot find the LoRa device")


# 找Gateway 
LoRa.FunLora_Node01_FindGateway()


## 等待資料進來
#LoRa.FunLora_BoardcaseRead()



"""
"""
#讀取F/W版本及Chip ID
print("Get Firmware Version, FunLora_0_GetChipID()")
LoRa.FunLora_0_GetChipID()
print("firmware Version= %d" % LoRa.firmwareVersion);

#Display Device ID 讀取設備的唯一碼
print("device ID= %d" % LoRa.deviceID);


# 重置 & 初始化
print("Init, FunLora_1_Init()")
LoRa.FunLora_1_Init()


# 讀取設定狀態
print("\n[4]:FunLora_2_ReadSetup");
LoRa.FunLora_2_ReadSetup();


# 設定寫入和頻段
print("\n[7]:FunLora_3_TX")
LoRa.FunLora_3_TX();

##寫入資料
#print("\n[10]:FunLora_5_write16bytesArray")
#LoRa.FunLora_5_write16bytesArray("abcdefghijklmnop");

##寫入資料
#print("\n[11]:FunLora_5_write16bytes")
#data=[ 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
#LoRa.FunLora_5_write16bytes(data);

#寫入資料
print("\n[12]:FunLora_5_writeString")
LoRa.FunLora_5_writeString("abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890");


#寫入資料
print("\n[13]:FunLora_5_writeStringWaitTillResponse")
LoRa.FunLora_5_writeStringWaitTillResponse("abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890");




"""



# 關閉
LoRa.FunLora_close() 


