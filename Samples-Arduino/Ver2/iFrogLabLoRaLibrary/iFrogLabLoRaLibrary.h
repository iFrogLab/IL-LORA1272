#ifndef iFrogLabLoRaLibrary_h
#define iFrogLabLoRaLibrary_h

#include <inttypes.h>

class iFrogLabLoRaLibrary
{

public:
  unsigned long m_lastTime;
  uint8_t m_pin;
  int m_brightness;
  int m_fadeAmount;
  unsigned long m_delayDuration;
  
  iFrogLabLoRaLibrary(void);
  void set(uint8_t pin, int initBrightness, int fadeAmount, unsigned long delayDuration);
  void update(void);
};

#endif
