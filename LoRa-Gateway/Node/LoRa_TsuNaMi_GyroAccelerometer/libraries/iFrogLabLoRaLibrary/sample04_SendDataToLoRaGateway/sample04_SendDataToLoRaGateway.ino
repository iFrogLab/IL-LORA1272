
/*
 * iFrogLab IL-LORA1272 
 * 功能,     ARDUINO , IFROGLAB LORA, IL-LORA1272
 * 電源,     3.3V    ,Pin 3, VDD
 * 接地,     GND     ,Pin 1, GND
 * 接收反應,  Pin 9   , Pin 2, Host_IRQ
 * UART,     Pin 10  ,UART_RX  Pin 7, UART_TX
 * UART,     Pin 11  ,UART_TX  Pin 8, UART_RX
 * 
 *　
 * LoRa Gateway的設定，請看　http://www.ifroglab.com/?p=7669
 */
#include <iFrogLabLoRaLibrary.h>
iFrogLabLoRaLibrary LoRa(10,11,9);  // RX, TX, DataReady

  byte t1[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
void setup()  {
  Serial.begin(9600);
  while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
  }
  
  byte TXRX=2;  // Mode : Sleep(0x00)、StandBy(0x01)、Tx(0x02)、Rx(0x03)。  
  // Freq : 輸入915.00MHz先轉成91500再轉16進位方式填入0x1656C -> 0x01 0x65 0x6C，SX1272範圍(860.00 ~ 1020.00MHz)，SX1276範圍(137.00 ~ 1020.00MHz)。
  byte Freq1=0x01;
  byte Freq2=0x65;
  byte Freq3=0x6c;
  byte Power =0x3;  // Power:125k(0x01)、250k(0x2)、500k(0x3)。Default 500K。 
  byte* data=LoRa.Setup(TXRX, Freq1, Freq2, Freq3, Power);//設定傳輸的頻率
  LoRa.WriteMode();      //設定LoRa為傳輸資料模式
}

void loop()  { 
  // 設定要傳遞的資料
  for(int i=0;i<=15;i++){
     t1[i] = random(255);
     Serial.print(t1[i]); 
  } 
  Serial.println("");
  LoRa.Write16bytesBroadcast(t1,16); //傳輸資料
  delay(1000);
}


