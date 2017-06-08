# python ap12-SendReceive-data.py -u /dev/tty.usbserial-A700eGFx -r 115200 -a T  -s a1,2,3,4,5
# python ap12-SendReceive-data.py -u /dev/tty.wchusbserial1410 -r 115200 -a R  
import serial
import sys, getopt
import time
import numpy
import RPi.GPIO as GPIO ## Import GPIO library

global_RXArray = 0
global_TXIndex = 0
global_RXCmd = 0


def FunRX(ser):
    global global_RXArray
    global global_RXCmd
    ser.write(serial.to_bytes([0xc1,0x03,0x05,0x03,0xe4,0xc0,0x00,0x03]))
    data = ser.read(5)
    print data.encode('hex')
    time.sleep(0.1)
    print ("reciver:")
    while True:
      ser.write(serial.to_bytes([0xc1,0x06,0x00]))
      data = ser.read(3)
      if len(data)>=2 :
        len1=int(data[2].encode('hex'),16)
        cmd = ser.read(1)
        data2 = ser.read(len1-1)
        CRC = ser.read(1)
        isSame=numpy.array_equal(data2,global_RXArray)
        #print (cmd,16)
        if isSame == False or global_RXCmd!=cmd :
           global_RXArray=data2
           global_RXCmd=cmd
           print data2.encode('hex')
           if data2[0] == 0x71:
              GPIO.output(7,True) ## Turn on GPIO pin 7
           elif data2[0] == 0x70:
              GPIO.output(7,False) ## Turn off GPIO pin 7
           elif data2[0] == 0xb1:
              GPIO.output(11,True) ## Turn on GPIO pin 7
           elif data2[0] == 0xb0:
              GPIO.output(11,False) ## Turn off GPIO pin 7
           #tarray=['0']
           #FunTX(ser,tarray)
      else:
        exit(2)

def FunTX(ser,data_array):
    global global_TXIndex
    t_mil=int(round(time.time() * 1000))%0xaf
    if global_TXIndex == t_mil:
       global_TXIndex=global_TXIndex+1
    else:
       global_TXIndex=t_mil
    FunTX_Send(ser,data_array,global_TXIndex)
    



def FunTX_Send(ser,data_array,TxIndex):    
    ser.write(serial.to_bytes([0xc1,0x03,0x05,0x02,0xe4,0xc0,0x00,0x03]))
    data = ser.read(5)
    print data.encode('hex')
    TX_Data=data_array
    #[0x01,0x02,0x03]
    CMD_Data=[0xc1,0x05]
    CMD_Data.append(len(TX_Data)+1)
    CMD_Data.append(TxIndex)
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
    ser.write(serial.to_bytes([0x80,0x00,0x00]))
    data = ser.read(6)
    print data.encode('hex')
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
      GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
      GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
      GPIO.setup(11, GPIO.OUT) ## Setup GPIO Pin 11 to OUT
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



