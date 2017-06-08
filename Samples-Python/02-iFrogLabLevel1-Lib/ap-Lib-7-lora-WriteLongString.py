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
LoRa2.FunLora_3_TX();

counter=0
while True:
  LoRa2.FunLora_5_writeString("abcdefghijklmnopqrstuvwxyz0123456789");
  counter=counter+1
  print(counter)
  #time.sleep(0.05)

# 關閉
LoRa2.FunLora_close()

