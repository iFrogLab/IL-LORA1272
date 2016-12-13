/*
 * 
 * iFrogLab IL-LORA1272 
 * 功能,     ARDUINO , IFROGLAB LORA, Function
 * 電源,     3.3V    ,Pin 3         , VDD
 * 接地,     GND     ,Pin 1         , GND
 * 接收反應,  Pin 9   , Pin 2        , Host_IRQ
 * UART,     Pin 10  ,UART_RX  Pin 7, UART_TX
 * UART,     Pin 11  ,UART_TX  Pin 8, UART_RX

 created back in the mists of time
 modified 25 May 2012
 by Tom Igoe
 based on Mikal Hart's example

 This example code is in the public domain.

 */
#include <SoftwareSerial.h>
int loopCounter=999999;
SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  Serial.println("Goodnight moon!");

  // set the data rate for the SoftwareSerial port
  mySerial.begin(115200);
  FunLora_0_GetChipID();
  delay(200);

  Serial.println("FunLora_1_Init");
  FunLora_1_Init();
  delay(200);
  Serial.println("FunLora_2_ReadSetup");
  FunLora_2_ReadSetup();  
  delay(200);

  Serial.println("-------Write");
  
  Serial.println("FunLora_3_Setup(2)");
  FunLora_3_Setup(2);
  delay(200);
  Serial.println("FunLora_5_write()");
  FunLora_5_write();
  delay(200);

  
  Serial.println("-------Read");
  Serial.println("FunLora_3_Setup(3)");
  FunLora_3_Setup(3);
  delay(200);
  Serial.println("FunLora_6_read()");
  FunLora_6_read();
  delay(200);


  
}

void loop() { // run over and over
  /*
  if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
  }
  if (Serial.available()) {
    mySerial.write(Serial.read());
  }*/
}


int i=0;
void FunLora_0_GetChipID(){
  byte t1[] = {0x80,0,0};
  mySerial.write(t1, 3);
  i=0;
  for(int j=0;j<loopCounter;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=6){
     Serial.println();
     return;
    }
   }
  }
}


void FunLora_1_Init(){
  byte t1[] = {0xc1,1,0};
  mySerial.write(t1, 3);
  i=0;
  for(int j=0;j<loopCounter;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=5){
     Serial.println();
     return;
    }
   }
  }
}




void FunLora_2_ReadSetup(){
  byte t1[] = {0xc1,2,0};
  mySerial.write(t1, 3);
  i=0;
  for(int j=0;j<loopCounter;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=12){
     Serial.println();
     return;
    }
   }
  }
}


void FunLora_3_Setup(byte TXRX){
  byte t1[] = {0xc1,0x03,0x05,TXRX,0xE4,0xC0,0x0,0x3};
  mySerial.write(t1, 8 );
  i=0;
  for(int j=0;j<loopCounter;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=5){
     Serial.println();
     return;
    }
   }
  }
}


void FunLora_5_write(){ //byte iData[]){
  byte t1[] = {0xc1,0x05,0x03,0x01,0x02,0x03};
  mySerial.write(t1, 8 );
  i=0;
  for(int j=0;j<loopCounter;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=12){
     Serial.println();
     return;
    }
   }
  }
}


void FunLora_6_read(){
  int dataLen=0;
  byte t1[] = {0xc1,0x06,0x0,0x00};
  mySerial.write(t1, 3 );
  i=0;
  for(int j=0;j<loopCounter;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
    if(i==3){
      dataLen=t1;
    }
     if(i>=(3+dataLen+1)){
     Serial.println();
     return;
    }
   }
  }
}








