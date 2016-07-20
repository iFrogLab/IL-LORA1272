import serial
import serial
    # ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 

try:
  ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=5)
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

  ser.write(serial.to_bytes([0xc1,0x03,0x05,0x03,0xe4,0xc0,0x00,0x03]))
  data = ser.read(5)
  print data.encode('hex')
 
  ser.write(serial.to_bytes([0xc1,0x06,0x00]))
  data = ser.read(7)
  print ("reciver:")
  print data.encode('hex')
  ser.close()        
except serial.serialutil.SerialException:
  print 'cannot open Serial Port'
