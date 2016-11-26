import serial
ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
ser.baudrate = 9600                     #Set baud rate to 9600
#data = ser.read(10)                     #Read ten characters from serial port to data
#ser.write("you send:")
#ser.write(data)                         #Send back the received data
ser.write(serial.to_bytes([0x4C,0x12,0x01,0x00,0x03,0x40,0xFB,0x02,0x7a]))
ser.close()        








