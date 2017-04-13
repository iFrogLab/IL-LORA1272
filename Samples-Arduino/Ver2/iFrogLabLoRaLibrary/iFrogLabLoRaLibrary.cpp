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
	m_Debug=1;
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

//////////////////////////
void iFrogLabLoRaLibrary::Fun_AddArray(byte source[],byte target[],int sourceLen,int targetStart){
   for(int i=0;i<sourceLen;i++){
       target[targetStart+i]=source[i];
   }
   return ;
}
byte iFrogLabLoRaLibrary::Fun_CRC(byte t1[], int len){
  byte CRC =0;
  for(int i=0;i<len;i++){
    CRC=CRC^t1[i]; // xor
  }
  return CRC;
}

void iFrogLabLoRaLibrary::Fun_PrintArray(byte t1[], byte len){
	
  Serial.print("Fun_PrintArray: ");
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
  Message_error();
  return data;
}
void iFrogLabLoRaLibrary::Message_error()
{
  Serial.println("Error:");
  Serial.println("Cannot find the iFrogLab LoRa device, please check hardware, RX, TX, 3.3V, GND.  ");
  Serial.println("mroe detail, please see hhttp://www.ifroglab.com/?p=7086 ");
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


byte* iFrogLabLoRaLibrary::Setup(byte TXRX,byte Freq1,byte Freq2,byte Freq3,byte Power){
  // byte t1[] = {0xc1,0x03,0x05,TXRX,0x01,0x65,0x6c,0x3};
  m_TXRX=TXRX;
  m_Freq1=Freq1;
  m_Freq2=Freq2;
  m_Freq3=Freq3;
  m_Power=Power;
  byte CRC=0;
  byte t1[] = {0xc1,0x03,0x05,TXRX,Freq1,Freq2,Freq3,Power,CRC};
  CRC=Fun_CRC(t1,8);
  t1[8] = CRC;
  mySerial->write(t1,9);
  if(m_Debug==1){
    Fun_PrintArray(t1,9);
    Serial.print("Recive: ");
  }
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial->available()) {
    byte t1=mySerial->read();
    Serial.print(t1, HEX);
    Serial.print(",");
    data[i]=t1;
    i=i+1;
    if(i>=5){ 
      if(m_Debug==1){
        Serial.println(" ");
        if(data[1]==0xAA) {  Serial.println("\n OK"); }
        else {  Serial.println("\n Error!"); return NULL;}
        Serial.println("\n------------------");
      }
      return data;
    }
   }
  }

  Message_error();
}

void iFrogLabLoRaLibrary::WriteMode(){
  m_TXRX=0x02;
  Setup(m_TXRX,m_Freq1,m_Freq2,m_Freq3,m_Power);
}

void iFrogLabLoRaLibrary::Write16bytesBroadcast(byte iData[],byte len){
  WriteMode();

  byte t2[16+1+3];
  byte CRC = 0; 
  // byte len=sizeof(iData) / sizeof(byte);  // sizeof(iData); //(byte)(iStr.length());
  //byte len1=len+1;
  if(len==0) return;

  
  // 定義碼
  byte t1[] = {0xc1,0x05,len};
  char charBuf[len*2+10];
  Fun_AddArray(t1,t2,3,0);

  // 字串轉char
  //char charBuf2[len*2];
  //iStr.toCharArray(charBuf2,len*2);
  
  //複製字串
  t2[2]=len;
  Fun_AddArray(iData,t2,(len*2)+2,3);

  //算CRC
  CRC=Fun_CRC(t2,3+len);  
  t2[3+len] = CRC;
  

  mySerial->write(t2,3+(len)+1);
  Fun_PrintArray(t2,3+(len)+1);
  if(m_Debug==1) Serial.print("Recive: ");

 
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial->available()) {
    byte t1=mySerial->read();
    if(m_Debug==1){
      Serial.print(t1, HEX);
      Serial.print(",");
    }
    i=i+1;
     if(i>=5){
        if(m_Debug==1){ 
          if(data[1]==0xAA ) { Serial.println("\n OK");   }
          else {  Serial.println("\n Error!");  }
        }
     return;
    }
   }
  }
  
  Message_error();

}
void iFrogLabLoRaLibrary::ReadMode(){
  m_TXRX=0x03;
  Setup(m_TXRX,m_Freq1,m_Freq2,m_Freq3,m_Power);
}


byte*  iFrogLabLoRaLibrary::Read16bytesBroadcast(){
  ReadMode();

  //byte t2[16+1+3];
  byte CRC = 0; 
  byte readLen=0;
  // byte len=sizeof(iData) / sizeof(byte);  // sizeof(iData); //(byte)(iStr.length());
  //byte len1=len+1;
  //if(len==0) return;

  
  // 定義碼
  byte t1[] = {0xc1,0x06,0x00,CRC};
  CRC=Fun_CRC(t1,3);  
  t1[3] = CRC;
  

  mySerial->write(t1,4);
  Fun_PrintArray(t1,4);
  if(m_Debug==1) Serial.print("Recive: ");

 
  i=0;
  int k=0;
  for(int j=0;j<999999;j++){
   if (mySerial->available()) {
    byte t1=mySerial->read();
    if(m_Debug==1) {
      Serial.print(t1, HEX);
      Serial.print(",");
    }
    data[i]=t1;
    i=i+1;
    if(i>=2){
      if(i>=3 && i<(readLen+2) ){
        data2[k]=t1;
        k=k+1;
      }
      if(i==3) {
        readLen=data[2];
        if(data[1]==0xFF ) {  
          if(m_Debug==1)Serial.println("\n Error!");  
          return;  
        }else if(data[1]!=0x86 ) { 
          if(m_Debug==1) Serial.println("\n Error!");   
          return;  
        }else {  
          if(m_Debug==1) Serial.println("\n OK"); 
        }
      }else if(i>=3+readLen+1)   {
        if(m_Debug==1){
          Serial.println(" ");
          Serial.println("\n------------------");
        }
        return data2;
      }
    }
   }
  }
  

  Message_error();
}





////////////////////////////////////////////////////

