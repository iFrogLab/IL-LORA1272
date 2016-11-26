import serial

import sys, getopt


def FunSerial(USBPort,USBRate):
  try:
    #ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=5)
    #ser = serial.Serial("/dev/cu.usbserial-A700eGFx", 115200, timeout=1)
    #ser = serial.Serial("/dev/cu.usbserial", 115200, timeout=1)
    print '----------------------------------'
    ser = serial.Serial(USBPort, USBRate, timeout=0.5)
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


def main(argv):
   USBPort = ''
   USBRate = 100
   try:
      opts, args = getopt.getopt(argv,"hu:r:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'xxx.py -u <USBPort> -r <USB Rate>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -u <USBPort> -r <USBRate>'
         sys.exit()
      elif opt in ("-u", "--ifile"):
         USBPort = arg
      elif opt in ("-r", "--ofile"):
         USBRate = arg
   print 'USB Port is ', USBPort
   print 'USB Rate is ', USBRate
   print 'xxx.py -u <USBPort> -u <USBRate>'
   FunSerial(USBPort,USBRate)


if __name__ == "__main__":
   main(sys.argv[1:])



