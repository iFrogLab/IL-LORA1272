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
範例3:
確認，二個LoRa 可以連續大量的　送　和　收資料
ap-Lib-5-lora-LoopRead.py
ap-Lib-5-lora-LoopWrite.py
"""

import ifroglab
import Queue
import threading
import urllib2




LoRa = ifroglab.LoRa()

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

LoRa.debug = False
counter = 0
while True:
    allData=LoRa.FunLora_6_read()
    counter=counter+1
    print("Read String Counter=%s" % str(counter))
    print ','.join('{:02x}'.format(x) for x in allData)






# 關閉
LoRa.FunLora_close()


