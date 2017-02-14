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
import httplib


def Fun_CRC(data):
    crc=0
    for i in data:
        crc=crc^i
    return crc

# Fun_HTTPGet("www.powenko.com","/download_release/get.php?name=powenko&password=12345")
def Fun_HTTPGet(iURL,iURLPath):
   httpClient = None
   try:
        response = httplib.HTTPConnection(iURL)  #"www.powenko.com")
        response.request("GET", iURLPath)   #"/download_release/get.php?name=powenko&password=12345")
        r1 = response.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        print(data1)
   except Exception, e:
        print(e)
   finally:
        if httpClient:
           httpClient.close()

def Fun_main():
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


    # 讀取設定狀態
    print("\n[4]:FunLora_2_ReadSetup");
    LoRa.FunLora_2_ReadSetup();

    # 設定寫入和頻段
    print("\n[7]:FunLora_3_TX")
    LoRa.FunLora_3_TX();

    #寫入資料：通知大家，Gateway 啟動了
    print("\n[10]:FunLora_5_write16bytesArray")
    LoRa.FunLora_5_write16bytesArray("D:iFL,G:S");

    # 設定讀取和頻段
    print("\n[7]:FunLora_3_RX")
    LoRa.FunLora_3_RX();

    #讀取資料
    print("\n[8]:FunLora_6_read")


    for t1 in range(60*60*24*365):     # 請整到實際的工作秒數
        ptint(t1)
        data=LoRa.FunLora_6_read();
        print(data)
        len1=len(data)
        print(len1)
        if len1>4:       
           for t1 in range(0,len1-3):                                                                                                                                                      
                print("data[%s]=%s,  Hex->%s"%(t1,data[t1+3],data[t1+3].encode('hex')))    
                x1=(int(data[t1+3].encode('hex'),16))
                urlData="localhost/AjaxIoT.php?action=insertByAPIKey&KeyName=%s&Data=%d&Datatype=1&APIKey=iloveifroglab"%(t1,x1);
                Fun_HTTPGet("127.0.0.1",urlData)  # 上傳資料          
        time.sleep(1)          
        

    # 關閉
    LoRa.FunLora_close() 
    ser.close()


# Start Main Program
Fun_main()


