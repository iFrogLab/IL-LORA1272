
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
  
  byte TXRX=3;  // Mode : Sleep(0x00)、StandBy(0x01)、Tx(0x02)、Rx(0x03)。  
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
  
}

void loop()  { 
  LoRa.ReadMode();    //讀取模式切換
  delay(10);
  byte* data2=LoRa.Read16bytesBroadcast();
  Serial.println("--------------------------");
  Serial.println(data2[0],HEX);
  Serial.println(data2[1],HEX);
  /*
  Serial.println(data2[2],HEX);
  Serial.println(data2[3],HEX);
  Serial.println(data2[4],HEX);
  Serial.println(data2[5],HEX);
  Serial.println(data2[6],HEX);
  Serial.println(data2[7],HEX);
  Serial.println(data2[8],HEX);
  Serial.println(data2[9],HEX);
  Serial.println(data2[10],HEX);
  Serial.println(data2[11],HEX);
  Serial.println(data2[12],HEX);
  Serial.println(data2[13],HEX);
  Serial.println(data2[14],HEX);
  Serial.println(data2[15],HEX);*/
 
  delay(1000);
}


