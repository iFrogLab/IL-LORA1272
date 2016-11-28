import serial
#ser = serial.Serial ("/dev/ttyAMA0")    #Open named port  RPI
ser = serial.Serial ("/dev/cu.usbserial")    #MAC port
ser.baudrate = 9600                     #Set baud rate to 9600
data = ser.read(10)                     #Read ten characters from serial port to data
ser.write("you send:")
ser.write(data)                         #Send back the received data
ser.close()        








