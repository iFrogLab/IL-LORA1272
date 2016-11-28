
/*
 * Pin 10 -> RX 
 * Pin 11 -> TX
 */
#include <iFrogLabLoRaLibrary.h>

#define LEDPIN 9

iFrogLabLoRaLibrary LoRa(10,11,9);  // RX, TX, DataReady
//byte* data[20];
void setup()  {
  Serial.begin(9600);
  while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
  }
  byte* data=LoRa.GetChipID();
 
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
    
   
}

void loop()  { 
}


