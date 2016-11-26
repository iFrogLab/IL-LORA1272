import serial
#ser = serial.Serial ("/dev/ttyAMA0")    #Open named port  RPI
ser = serial.Serial ("/dev/cu.usbserial")    #Open named port 
ser.baudrate = 115200                     #Set baud rate to 9600

#data = ser.read(10)                     #Read ten characters from serial port to data
#ser.write("you send:")
#ser.write(data)                         #Send back the received data
ser.write(serial.to_bytes([0x80,0x00,0x00,0x80]))
data = ser.read(10)
#ser.write(data)
print(data)
print data.encode('hex')
ser.close()        








