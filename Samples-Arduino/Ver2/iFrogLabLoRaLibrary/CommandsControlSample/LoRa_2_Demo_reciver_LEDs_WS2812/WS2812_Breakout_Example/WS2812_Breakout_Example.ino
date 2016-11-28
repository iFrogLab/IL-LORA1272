/* SparkFun WS2812 Breakout Board Example
  SparkFun Electronics
  date: July 25, 2013
  license: GNU GENERAL PUBLIC LICENSE
  
  Requires the Adafruit NeoPixel library. It's awesome, go get it.
  https://github.com/adafruit/Adafruit_NeoPixel
  
  This simple example code runs three sets of animations on a group of WS2812
  breakout boards. The more boards you link up, the better these animations
  will look. 
  
  For help linking WS2812 breakouts, checkout our hookup guide:
  https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide
  
  Before uploading the code, make sure you adjust the two defines at the
  top of this sketch: PIN and LED_COUNT. Pin should be the Arduino pin
  you've got connected to the first pixel's DIN pin. By default it's
  set to Arduino pin 4. LED_COUNT should be the number of breakout boards
  you have linked up.
*/

#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>
#include "WS2812_Definitions.h"

#define PIN 4
#define LED_COUNT 30

// Create an instance of the Adafruit_NeoPixel class called "leds".
// That'll be what we refer to from here on...
Adafruit_NeoPixel leds = Adafruit_NeoPixel(LED_COUNT, PIN, NEO_GRB + NEO_KHZ800);

byte data[20];
SoftwareSerial mySerial(10, 11); // RX, TX for UNO and MEGA
String LastString="";
void setup()
{
  leds.begin();  // Call this to start up the LED strip.
  clearLEDs();   // This function, defined below, turns all LEDs off...
  leds.show();   // ...but the LEDs don't actually update until you call this.
  
  /////           
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
  Serial.println("\n[6]:FunLora_6_read");
  FunLora_6_read();
  /*
  Serial.println("\n[7]:FunLora_3_TX");
  FunLora_3_TX();
  //Serial.println("\n[8]:FunLora_5_write");
  //FunLora_5_write_test("");
  
  Serial.println("\n[8]:FunLora_5_write");
  String stringOne="abcde";
  FunLora_5_write(stringOne);
  */
  Serial.println("\n[x]:End");
  
}
void loop()
{
  int x=255;
  int y=255;


  //byte data[20];
  FunLora_6_read();
  delay(200);
  
  x=data[5];
  x=data[6];
  //  設定LED 燈
  Serial.println(x);
  FunLed(x,y); 
  delay(200);
  
}

// Sets all LEDs to off, but DOES NOT update the display;
// call leds.show() to actually turn them off after this.
void clearLEDs()
{
  for (int i=0; i<LED_COUNT; i++)
  {
    leds.setPixelColor(i, 0);
  }
}

void FunLed(int x, int y){ 
  //int val = map(xl, 0, 255, 0, LED_COUNT);
  for (int i=0; i<LED_COUNT; i++)
  {
    leds.setPixelColor(i,0, x, 0); 
  }
  leds.show();  // Turn the LEDs on
}



//////////////////////////

byte Fun_CRC(byte t1[], int len){
  byte CRC =0;
  for(int i=0;i<len;i++){
    CRC=CRC^t1[i]; // xor
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
     if(i>=10){
      Serial.println(" ");
      Serial.print("\nChip:");
      Serial.println(data[3],HEX);
      Serial.print("FW_Ver:");
      Serial.println(data[4],HEX);
      Serial.print("Unique number:");
      Serial.print(data[5],HEX);
      Serial.print(data[6],HEX);
      Serial.print(data[7],HEX);
      Serial.println(data[8],HEX);
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



void Fun_AddArray(byte source[],byte target[],int sourceLen,int targetStart){
   for(int i=0;i<sourceLen;i++){
       target[targetStart+i]=source[i];
   }
   return ;
}
void FunLora_5_write(String iStr){ //byte iData[]){

  byte t2[16+1+3];
  byte CRC = 0; 
  byte len=(byte)(iStr.length());
  byte len1=len+1;
  if(len==0) return;

  
  // 定義碼
  byte t1[] = {0xc1,0x05,len1};
  char charBuf[len*2+10];
  Fun_AddArray(t1,t2,3,0);

  // 字串轉char
  char charBuf2[len*2];
  iStr.toCharArray(charBuf2,len*2);
  
  //複製字串
  t2[2]=len;
  Fun_AddArray(charBuf2,t2,(len*2)+2,3);

  //算CRC
  CRC=Fun_CRC(t2,3+len);  
  t2[3+len] = CRC;
  

  mySerial.write(t2,3+(len)+1);
  Fun_PrintArray(t2,3+(len)+1);
  Serial.print("Recive: ");

 
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=5){
        if(data[1]==0xAA ) { Serial.println("\n OK");   }
        else {  Serial.println("\n Error!");  }
     return;
    }
   }
  }
  
  
}

void FunLora_5_write_v0(String iStr){ //byte iData[]){

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
        if(data[1]==0xFF ) {  Serial.println("\n Error!");   }
        else {  Serial.println("\n OK"); }
     return;
    }
   }
  }
  
  
}
//測試　write
void FunLora_5_write_test(String iStr){ //byte iData[]){

  byte CRC = 0; 


  //byte t1[] = {0xc1,0x05,len1};
  byte t1[] = {0xc1,0x05,3,0x31,0x32,0x33,0};
  CRC=Fun_CRC(t1,6);
  t1[6]=CRC;
  mySerial.write(t1,7);
  Fun_PrintArray(t1,7);
 
  i=0;
  for(int j=0;j<999999;j++){
   if (mySerial.available()) {
    byte t1=mySerial.read();
    Serial.print(t1, HEX);
    Serial.print(",");
    i=i+1;
     if(i>=5){
     //Serial.println();
        if(data[1]==0xFF ) {  Serial.println("\n Error!");   }
        else {  Serial.println("\n OK"); }
     return;
    }
   }
  }
  
  
}

void FunLora_6_read(){

  byte CRC=0;
  byte t1[] = {0xc1,0x06,0x00,CRC};
  byte readLen=0;
  CRC=Fun_CRC(t1,3);
  t1[3] = CRC;
  mySerial.write(t1,4);
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
    if(i>=2){
      if(i==3) {
        readLen=data[2];
        if(data[1]==0xFF ) {  Serial.println("\n Error!");  return;  }
        else if(data[1]!=0x86 ) {  Serial.println("\n Error!");   return;  }
        else {  Serial.println("\n OK"); }
        
      }else if(i>=3+readLen+1)   {
        Serial.println(" ");
        Serial.println("\n------------------");
        return data;
      }
    }
   }
  }

}



