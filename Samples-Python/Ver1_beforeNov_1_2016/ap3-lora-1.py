import serial
#ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 

#port_path="/dev/cu.usbserial"
port_path="/dev/cttyAMA0"
ser = serial.Serial (port_path)    #Open named port 

ser.baudrate = 115200                     #Set baud rate to 9600

#data = ser.read(10)                     #Read ten characters from serial port to data
#ser.write("you send:")
#ser.write(data)                         #Send back the received data
ser.write(serial.to_bytes([0x80,0x00,0x00]))
data = ser.read(5)
#ser.write(data)
print(data)
print data.encode('hex')
ser.close()        








