import serial
ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
ser.baudrate = 115200                     #Set baud rate to 9600

#data = ser.read(10)                     #Read ten characters from serial port to data
#ser.write("you send:")
#ser.write(data)                         #Send back the received data
ser.write(serial.to_bytes([0x80,0x00,0x00]))
data = ser.read(6)
#print(data)
print data.encode('hex')
ser.write(serial.to_bytes([0xc1,0x01,0x00]))
data = ser.read(5)
print data.encode('hex')
ser.write(serial.to_bytes([0xc1,0x02,0x00]))
data = ser.read(12)
print data.encode('hex')

ser.close()        








