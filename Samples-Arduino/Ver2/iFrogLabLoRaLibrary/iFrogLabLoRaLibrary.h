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




  byte* iFrogLabLoRaLibrary::Setup(byte TXRX,byte Freq1,byte Freq2,byte Freq3,byte Power);
  void iFrogLabLoRaLibrary::WriteMode();
  void iFrogLabLoRaLibrary::Write16bytesBroadcast(byte t1[],byte len);
  void iFrogLabLoRaLibrary::ReadMode();
  byte*  iFrogLabLoRaLibrary::Read16bytesBroadcast();
  void iFrogLabLoRaLibrary::ReadClear();


  //void set(uint8_t pin, int initBrightness, int fadeAmount, unsigned long delayDuration);
  //void update(void);

  //byte* GetChipID();
  //byte* iFrogLabLoRaLibrary::GetChipID();
  //SoftwareSerial mySerial(10, 11); 
  SoftwareSerial *mySerial;
  byte m_TXRX;
  byte m_Freq1;
  byte m_Freq2;
  byte m_Freq3;
  byte m_Power;

  uint8_t m_FW_Ver=6;
  uint32_t m_UniqueNumber=0;





private:

  byte  Fun_CRC(byte t1[], int len);   //計算出CRC 
  void  Fun_PrintArray(byte t1[], byte len);
  void  Fun_AddArray(byte source[],byte target[],int sourceLen,int targetStart);

  void iFrogLabLoRaLibrary::Message_error();

  unsigned long m_lastTime;
  uint8_t m_pin;
  int m_brightness;
  int m_fadeAmount;
  unsigned long m_delayDuration;

  byte data[30];
  byte data2[20];
  int i=0;
  uint8_t m_RX;
  uint8_t m_TX;
  int m_Debug;

};

#endif
