#ifndef iFrogLabLoRaLibrary_h
#define iFrogLabLoRaLibrary_h

#include <inttypes.h>
#include <SoftwareSerial.h>


//SoftwareSerial mySerial(10, 11); // RX, TX for UNO and MEGA
class iFrogLabLoRaLibrary
{

public:


  
  iFrogLabLoRaLibrary(int RX, int TX,int DataReady);
  //iFrogLabLoRaLibrary(int DataReady);
  byte* iFrogLabLoRaLibrary::GetChipIDAll();
  int iFrogLabLoRaLibrary::GetChipID();
  int iFrogLabLoRaLibrary::GetFirmwareVersion();
  int iFrogLabLoRaLibrary::GetDeviceID();


  //void set(uint8_t pin, int initBrightness, int fadeAmount, unsigned long delayDuration);
  //void update(void);

  //byte* GetChipID();
  //byte* iFrogLabLoRaLibrary::GetChipID();
  //SoftwareSerial mySerial(10, 11); 
  SoftwareSerial *mySerial;




private:

  byte  Fun_CRC(byte t1[], int len);   //計算出CRC 
  //void  Serial_print(char MSG);
  void  Fun_PrintArray(byte t1[], byte len);








  unsigned long m_lastTime;
  uint8_t m_pin;
  int m_brightness;
  int m_fadeAmount;
  unsigned long m_delayDuration;

  byte data[20];
  int i=0;
  uint8_t m_RX;
  uint8_t m_TX;
  int m_Debug;

};

#endif
