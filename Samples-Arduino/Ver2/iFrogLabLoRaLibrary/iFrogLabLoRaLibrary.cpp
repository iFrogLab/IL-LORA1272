// For Arduino 1.0 and earlier
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include "iFrogLabLoRaLibrary.h"

//SoftwareSerial mySerial(10, 11);
iFrogLabLoRaLibrary::iFrogLabLoRaLibrary(int RX, int TX, int DataReady)
{
	m_Debug=0;
  m_RX=RX;
  m_TX=TX;

	static SoftwareSerial mySerial2(m_RX,m_TX);    //setup RX, TX Pin
    mySerial=&mySerial2;
    //mySerial(10, 11); 
  	//mySerial.setTX(TX);
  	//mySerial.setRX(RX);
   mySerial->begin(115200); 


  	if(m_Debug==1){
      Serial.begin(9600);
      while (!Serial) {
            ; // wait for serial port to connect. Needed for native USB port only
      }
  		 
  	}

}

/*
void iFrogLabLoRaLibrary::set(uint8_t pin, int initBrightness, int fadeAmount, unsigned long delayDuration)
{
	m_pin = pin;
	m_brightness = initBrightness;
	m_fadeAmount = fadeAmount;
	m_delayDuration = delayDuration;
	
	pinMode(m_pin, OUTPUT);
	analogWrite(m_pin, m_brightness);
	m_lastTime = millis();
}
void iFrogLabLoRaLibrary::update(void)
{
	unsigned long t = millis();
	if(t > m_lastTime + m_delayDuration){
		m_lastTime += m_delayDuration;
		
		analogWrite(m_pin, m_brightness);
		m_brightness = m_brightness + m_fadeAmount;
	
		if (m_brightness <= 0 || m_brightness >= 255) {
			m_fadeAmount = -m_fadeAmount;
		}
	}
}*/
//////////////////////////

byte iFrogLabLoRaLibrary::Fun_CRC(byte t1[], int len){
  byte CRC =0;
  for(int i=0;i<len;i++){
    CRC=CRC^t1[i]; // xor
  }
  return CRC;
}

void iFrogLabLoRaLibrary::Fun_PrintArray(byte t1[], byte len){
	
  if(m_Debug==1){
    Serial.print("Send:  ");
    for(byte i=0;i<len;i++){
      Serial.print(t1[i],HEX);
      Serial.print(",");
    }
    Serial.print("");
  }

}

byte* iFrogLabLoRaLibrary::GetChipIDAll()
{

  byte CRC = 0; 
  byte t1[] = {0x80,0,0,CRC};
  CRC=Fun_CRC(t1,3);
  t1[3] = CRC;

  mySerial->write(t1, 4);
  Fun_PrintArray(t1,4);
  if(m_Debug==1) Serial.print("Recive: ");
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial->available()) {
    byte t1=mySerial->read();
    if(m_Debug==1){
       Serial.print(t1,HEX);
       Serial.print(",");
    }
    data[i]=t1;
    i=i+1;
     if(i>=10){
      if(m_Debug==1){
        Serial.println(" ");
        Serial.print("\nChip:");
        Serial.println(data[3],HEX);
        Serial.print("FW_Ver:");
        Serial.println(data[4],HEX);
        Serial.print("Unique number:");
        Serial.print(data[5],HEX);
        Serial.print(data[6],HEX);
        Serial.print(data[7],HEX);
        Serial.print(data[8],HEX);
        Serial.println("\n------------------");
      }
     return data;
    }
    j++;
   }
  }

  return data;
}
int iFrogLabLoRaLibrary::GetChipID()
{
  GetChipIDAll();
  return data[3];
}
int iFrogLabLoRaLibrary::GetFirmwareVersion()
{
  GetChipIDAll();
  return data[4];
}
int iFrogLabLoRaLibrary::GetDeviceID()
{
  GetChipIDAll();
  int t1=(data[5]<<(8*3))+(data[6]<<(8*2))+(data[7]<<8)+(data[8]);
  return t1;
}
////////////////////////////////////////////////////

