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
print data.encode('hex')




# 重置 & 初始化
array2=[0xc1,0x01,0x00,0]
array2[3]=Fun_CRC(array2)
print array2
ser.write(serial.to_bytes(array2))
data = ser.read(5)
print data.encode('hex')



# 讀取設定狀態
array3=[0xc1,0x02,0x00,0]
array3[3]=Fun_CRC(array3)
print array3
ser.write(serial.to_bytes(array3))
data = ser.read(12)
print data.encode('hex')

#設定模式與頻率
#array4=[0xC1,0x3,0x5,0x3,0x1,0x65,0x6C,0x3,0]
array4=[0xC1,3,5,3,1,0x65,0x6C,0x3,0]
array4[8]=Fun_CRC(array4)
print array4
ser.write(serial.to_bytes(array4))
data = ser.read(5)
print data.encode('hex')

#資料
array5=[0xC1,0x6,0x0,0]
array5[3]=Fun_CRC(array5)
print array5
ser.write(serial.to_bytes(array5))
data = ser.read(3)
print data.encode('hex')
len=data[2]
data2 = ser.read(len)
print data2.encode('hex')





ser.close()        








