# www.ifroglab.com
# -*- coding: utf8 -*-
import ifroglab
import time
import serial

def Fun_CRC(data):
    crc=0
    for i in data:
        crc=crc^i
    return crc

LoRa = ifroglab.LoRa()


# 打開Port
print("Open Port, FunLora_init()")
ser=LoRa.FunLora_init()

#讀取F/W版本及Chip ID
print("Get Firmware Version, FunLora_0_GetChipID()")
LoRa.FunLora_0_GetChipID()

# 重置 & 初始化
print("Init, FunLora_1_Init()")
LoRa.FunLora_1_Init()



# 關閉
LoRa.FunLora_close() 
ser.close()

