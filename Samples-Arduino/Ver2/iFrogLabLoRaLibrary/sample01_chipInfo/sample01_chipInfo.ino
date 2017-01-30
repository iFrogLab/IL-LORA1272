
/*
 * iFrogLab IL-LORA1272 
 * Function功能,     ARDUINO , IFROGLAB LORA IL-LORA1272
 * GND接地,          GND     ,Pin 1, 
 * Host_IRQ接收反應, Pin 9   ,Pin 2, 
 * VDD電源,          3.3V    ,Pin 3, 
 * UART TX,         Pin 10  ,Pin 7 
 * UART RX,         Pin 11  ,Pin 8 
 * 
 * tutorial: please see http://www.ifroglab.com/?p=7641
 */
#include <iFrogLabLoRaLibrary.h>
iFrogLabLoRaLibrary LoRa(10,11,9);  // RX, TX, DataReady
void setup()  {
  Serial.begin(9600);
  byte* data=LoRa.GetChipIDAll();
  
  Serial.print("\nChip:");
  Serial.println(data[3],HEX);
    
  Serial.print("FW_Ver:");
  Serial.println(data[4],HEX);
  
  Serial.print("Unique number:");
  Serial.print(data[5],HEX);
  Serial.print(data[6],HEX);
  Serial.print(data[7],HEX);
  Serial.println(data[8],HEX);
    
  int ChipID=LoRa.GetChipID();
  Serial.print("ChipID:");
  Serial.println(ChipID);
  
  int firmwareVersion=LoRa.GetFirmwareVersion();
  Serial.print("Firmware VersionID:");
  Serial.println(firmwareVersion);
  
  int DeviceID=LoRa.GetDeviceID();
  Serial.print("DeviceID:");
  Serial.println(DeviceID);
  
}

void loop()  { 
}


