# python ap12-SendReceive-data.py -u /dev/tty.usbserial-A700eGFx -r 115200 -a T  -s a1,2,3,4,5
# python ap12-SendReceive-data.py -u /dev/tty.wchusbserial1410 -r 115200 -a R  
import serial
import sys, getopt
import time

def FunRX(ser):
    ser.write(serial.to_bytes([0xc1,0x03,0x05,0x03,0xe4,0xc0,0x00,0x03]))
    data = ser.read(5)
    print data.encode('hex')
    time.sleep(0.1)
    ser.write(serial.to_bytes([0xc1,0x06,0x00]))
    data = ser.read(3)
    print ("reciver:")
    print data.encode('hex')
    print ("data:")
    #print (data[2],hex)
    #print(data[2].encode('hex'))
    data2 = ser.read(int(data[2].encode('hex'),16))
    print data2.encode('hex')
    
   

def FunTX(ser,data_array):
    ser.write(serial.to_bytes([0xc1,0x03,0x05,0x02,0xe4,0xc0,0x00,0x03]))
    data = ser.read(5)
    print data.encode('hex')

    TX_Data=data_array
    #[0x01,0x02,0x03]
    CMD_Data=[0xc1,0x05]
    CMD_Data.append(len(TX_Data))
    for i3 in data_array:
       CMD_Data.append(int(i3, 16))
    #ser.write(serial.to_bytes([0xc1,0x05,0x03,0x01,0x02,0x03]))
    print(CMD_Data)
    #ser.write(serial.to_bytes(TX_Data))
    ser.write(CMD_Data)

    print ("Send:")
    #print ','.join(format(x, '02x') for x in serial.to_bytes(TX_Data))
    print ','.join([i2 for i2 in TX_Data])
    data = ser.read(5)
    print data.encode('hex')


  

def FunSerial(USBPort,USBRate,SendReceive,data_array):
  try:
    #ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=5)
    #ser = serial.Serial("/dev/cu.usbserial-A700eGFx", 115200, timeout=1)
    #ser = serial.Serial("/dev/cu.usbserial", 115200, timeout=1)
    print '----------------------------------'
    ser = serial.Serial(USBPort, USBRate, timeout=0.5)
    #ser.write(serial.to_bytes([0x80,0x00,0x00]))
    #data = ser.read(6)
    #print data.encode('hex')
    ser.write(serial.to_bytes([0xc1,0x01,0x00]))
    data = ser.read(5)
    print data.encode('hex')
    #time.sleep(0.1)
    ser.write(serial.to_bytes([0xc1,0x02,0x00]))
    data = ser.read(12)
    print data.encode('hex')
    #time.sleep(0.1)
    if   SendReceive == 'R':
       FunRX(ser)
    else:
       FunTX(ser,data_array)


    ser.close()        
  except serial.serialutil.SerialException:
    print 'cannot open Serial Port'




def main(argv):
   RXTX = 'aaaa'
   USBPort = ''
   USBRate = 100
   data_array=''
   try:
      opts, args = getopt.getopt(argv,"u:r:a:s:x",["ifile=","ofile=","action=","data_array=","xxx="])
   except getopt.GetoptError:
      print 'xxx.py -u <USBPort> -r <USB Rate> -a <R or T> -s "1,2,3,4,5"  '
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -u <USBPort> -r <USBRate>'
         sys.exit()
      elif opt in ("-u", "--ifile"):
         USBPort = arg
      elif opt in ("-r", "--ofile"):
         USBRate = arg
      elif opt in ("-a", "--Action"):
         RXTX = arg
      elif opt in ("-s", "--data_array"):
         data_array = arg
   print 'USB Port is ', USBPort
   print 'USB Rate is ', USBRate
   print 'RXTX Action is ', RXTX
   if len(data_array) > 0:
       data_array=data_array.split(',')
   print 'data_array Action is ', data_array
   print 'xxx.py -u <USBPort> -u <USBRate> -a <R or T> -s<11,12,13>'
   #data_array = [0x11,0x22,0x33]
   FunSerial(USBPort,USBRate,RXTX,data_array)


if __name__ == "__main__":
   main(sys.argv[1:])



