
# coding=UTF-8
# * iFrogLab IL-LORA1272  www.ifroglab.com
# *
# * 功能,             USB to TTL , IFROGLAB LORA 
# * 電源VDD,          3.3V       ,Pin 3         
# * 接地GND,          GND        ,Pin 1        
# * 接收反應Host_IRQ,  null       , Pin 2        
# * UART,             RX         ,UART_RX  Pin 7 
# * UART,             TX         ,UART_TX  Pin 8 



import serial
import platform
#ser = serial.Serial ("/dev/ttyAMA0")    #Open named port  RPI
OSVersion=platform.system()
port_path="/dev/cu.usbserial"
print OSVersion
if OSVersion=="Darwin":
	port_path="/dev/cu.usbserial"
#ser = serial.Serial ("/dev/ttyAMA0")    #Open named port  RPI
ser = serial.Serial ("/dev/cu.usbserial")    #MAC port
ser.baudrate = 115200                     #Set baud rate to 9600
#data = ser.read(1)                     #Read ten characters from serial port to data
#ser.write("you send:")
#ser.write(data)                         #Send back the received data
ser.close()        








