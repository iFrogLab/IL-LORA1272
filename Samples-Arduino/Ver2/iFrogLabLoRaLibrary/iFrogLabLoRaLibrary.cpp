// For Arduino 1.0 and earlier
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include "iFrogLabLoRaLibrary.h"

iFrogLabLoRaLibrary::iFrogLabLoRaLibrary(void)
{
}

void iFrogLabLoRaLibrary::set(uint8_t pin, int initBrightness, int fadeAmount, unsigned long delayDuration)
{
	m_pin = pin;
	m_brightness = initBrightness;
	m_fadeAmount = fadeAmount;
	m_delayDuration = delayDuration;
	
	pinMode(m_pin, OUTPUT);
	analogWrite(m_pin, m_brightness);
	m_lastTime = millis();
}


void iFrogLabLoRaLibrary::update(void)
{
	unsigned long t = millis();
	if(t > m_lastTime + m_delayDuration){
		m_lastTime += m_delayDuration;
		
		analogWrite(m_pin, m_brightness);
		m_brightness = m_brightness + m_fadeAmount;
	
		if (m_brightness <= 0 || m_brightness >= 255) {
			m_fadeAmount = -m_fadeAmount;
		}
	}
}

