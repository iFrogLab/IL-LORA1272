
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
  byte* data=LoRa.GetChipIDAll();
 
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
    
   
  Serial.println("");
  Serial.println("--------------------------");
  Serial.println("");
  int ChipID=LoRa.GetChipID();
  Serial.print("ChipID:");
  Serial.print(ChipID);
  
  Serial.println("");
  int firmwareVersion=LoRa.GetFirmwareVersion();
  Serial.print("Firmware VersionID:");
  Serial.print(firmwareVersion);

  
  Serial.println("");
  int DeviceID=LoRa.GetDeviceID();
  Serial.print("DeviceID:");
  Serial.print(DeviceID);
  
  
}

void loop()  { 
}


