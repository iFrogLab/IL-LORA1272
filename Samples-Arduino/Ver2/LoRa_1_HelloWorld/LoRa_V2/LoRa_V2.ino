/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
 */
#include <SoftwareSerial.h>


SoftwareSerial mySerial(10, 11); // RX, TX
String LastString="";
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(13, OUTPUT);

  Serial.begin(9600);     // set the dta rate for the Serial port
  mySerial.begin(115200); // set the data rate for the SoftwareSerial port
  
  Serial.println("\n[1]:Start");
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("\n[2]:FunLora_0_GetChipID");
  FunLora_0_GetChipID();
  Serial.println("\n[3]:FunLora_1_Init");
  FunLora_1_Init();
  Serial.println("\n[4]:FunLora_2_ReadSetup");
  FunLora_2_ReadSetup();
  Serial.println("\n[5]:FunLora_3_RX");
  FunLora_3_RX();
  Serial.println("\n[5]:FunLora_3_TX");
  FunLora_3_TX();
  Serial.println("\n[6]:FunLora_5_write");
  String stringOne="Hello";
  FunLora_5_write(stringOne);
 
  Serial.println("\n[x]:End");
 
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(200);              // wait for a second
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
  delay(200);              // wait for a second
}

//////////////////////////

byte Fun_CRC(byte t1[], int len){
  byte CRC =0;
  for(int i=0;i<len;i++){
    CRC=CRC^t1[i];
  }
 
  return CRC;
}
void Fun_PrintArray(byte t1[], byte len){
  Serial.print("Send:  ");
  for(byte i=0;i<len;i++){
    Serial.print(t1[i], HEX);
    Serial.print(",");
  }
  Serial.println("");
}
byte data[10];
int i=0;
// Gett Drvice Version
void FunLora_0_GetChipID(){       
  byte CRC = 0; 
  byte t1[] = {0x80,0,0,CRC};
  CRC=Fun_CRC(t1,3);
  t1[3] = CRC;
  mySerial.write(t1, 4);
  Fun_PrintArray(t1,4);
  Serial.print("Recive: ");
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    data[i]=t1;
    i=i+1;
     //if(i>=7+3){
     if(i>=7){
      Serial.println(" ");
      Serial.print("\nChip:");
      Serial.println(data[3],HEX);
      Serial.print("FW_Ver:");
      Serial.println(data[4],HEX);
      Serial.println("\n------------------");
     return;
    }
    j++;
   }
  }
}

// Init & reset default 
void FunLora_1_Init(){
       
  byte CRC = 0; 
  byte t1[] = {0xc1,1,0,CRC};
  CRC=Fun_CRC(t1,3);
  t1[3] = CRC;
  mySerial.write(t1, 4);
  Fun_PrintArray(t1,4);
  Serial.print("Recive: ");
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    data[i]=t1;
    i=i+1;
     if(i>=5){
      Serial.println(" ");
      if(data[1]==0xAA) {  Serial.println("\nRset OK"); }
      else {  Serial.println("\nRset Error!"); }
      Serial.println("\n------------------");
     return;
    }
   }
  }
}
// 讀取設定
void FunLora_2_ReadSetup(){

  byte CRC =  0xc1 ^ 2 ^ 0; 
  byte t1[] = {0xc1,2,0,CRC};
  mySerial.write(t1, 4);
  Fun_PrintArray(t1,4);
  Serial.print("Recive: ");
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    data[i]=t1;
    i=i+1;
    if(i>=12){
      Serial.println(" ");
      Serial.print("Mode:");
      Serial.println(data[3],HEX);
      Serial.print("Frg:");
      Serial.print(data[4],HEX); Serial.print(",");
      Serial.print(data[5],HEX); Serial.print(",");
      Serial.println(data[6],HEX);
      Serial.print("Power:");
      Serial.println(data[7],HEX);
      Serial.println("\n------------------");
      return;
    }
   }
  }
}

void FunLora_3_Setup(byte TXRX,byte Freq1,byte Freq2,byte Freq3,byte Power){
  // byte t1[] = {0xc1,0x03,0x05,TXRX,0x01,0x65,0x6c,0x3};
  byte CRC=0;
  byte t1[] = {0xc1,0x03,0x05,TXRX,Freq1,Freq2,Freq3,Power,CRC};
  CRC=Fun_CRC(t1,8);
  t1[8] = CRC;
  mySerial.write(t1,9);
  Fun_PrintArray(t1,9);
  Serial.print("Recive: ");
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    data[i]=t1;
    i=i+1;
    if(i>=5){ 
      Serial.println(" ");
      if(data[1]==0xAA) {  Serial.println("\n OK"); }
      else {  Serial.println("\n Error!"); }
      Serial.println("\n------------------");
     return;
    }
   }
  }
}

void FunLora_3_TX(){
  byte TXRX=0x02;
  FunLora_3_Setup(TXRX,0x01,0x65,0x6c,0x3);
}
void FunLora_3_RX(){
  byte TXRX=0x03;
  FunLora_3_Setup(TXRX,0x01,0x65,0x6c,0x3);
}



void FunLora_5_write(String iStr){ //byte iData[]){

  byte CRC = 0; 
  byte len=(byte)(iStr.length());
  byte len1=len+1;
  if(len==0) return;

  byte t1[] = {0xc1,0x05,len1};
  CRC=Fun_CRC(t1,2);
  mySerial.write(t1,2);
  Fun_PrintArray(t1,2);
  
  char charBuf[len+2];
  iStr.toCharArray(charBuf,len1);
  //Serial.println(iStr);
  //mySerial.write(charBuf,len);
  charBuf[len+1]=CRC;
  mySerial.write(charBuf,len1);
  Fun_PrintArray(charBuf,len1);

  
  Serial.print("Recive: ");

 
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=5){
     //Serial.println();
     return;
    }
   }
  }
  
  
}



