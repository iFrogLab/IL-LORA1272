
/*
 * iFrogLab IL-LORA1272 
 * 功能,     ARDUINO , IFROGLAB LORA, IL-LORA1272
 * 電源,     3.3V    ,Pin 3, VDD
 * 接地,     GND     ,Pin 1, GND
 * 接收反應,  Pin 9   , Pin 2, Host_IRQ
 * UART,     Pin 10  ,UART_RX  Pin 7, UART_TX
 * UART,     Pin 11  ,UART_TX  Pin 8, UART_RX
 */
#include <iFrogLabLoRaLibrary.h>
iFrogLabLoRaLibrary LoRa(10,11,9);  // RX, TX, DataReady
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
  
  byte* data=LoRa.Setup(TXRX, Freq1, Freq2, Freq3, Power);
  //();
 
  Serial.print("Return:");
  Serial.print(data[0],HEX);
  Serial.print(data[1],HEX);
  Serial.print(data[2],HEX);
  Serial.print(data[3],HEX);
    
  Serial.println("");
  Serial.println("--------------------------");
  Serial.println("");
  
  //LoRa.WriteMode();    //寫入資料
  byte t1[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
  LoRa.Write16bytesBroadcast(t1,16);
  
}

void loop()  { 
}


