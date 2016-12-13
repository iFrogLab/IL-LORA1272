# www.ifroglab.com
# -*- coding: utf8 -*-
import serial

def Fun_CRC(data):
    crc=0
    for i in data:
        crc=crc^i
    return crc



#ser = serial.Serial ("/dev/ttyAMA0")    # Raspbeeey Pi port
ser = serial.Serial ("/dev/cu.usbserial")    #MAC port
ser.baudrate = 115200                     #Set baud rate to 9600

#讀取F/W版本及Chip ID
array1=[0x80,0x00,0x00,0]
array1[3]=Fun_CRC(array1)
print array1
ser.write(serial.to_bytes(array1))
data = ser.read(10)
#print(data)
print data.encode('hex')

# 重置 & 初始化
array2=[0xc1,0x01,0x00,0]
array2[3]=Fun_CRC(array2)
print array2
ser.write(serial.to_bytes(array2))
data = ser.read(5)
print data.encode('hex')
ser.close()        








