#include <PwmLed.h>

#define LEDPIN 9

PwmLed pwmled;

void setup()  {
  pwmled.set(LEDPIN, 0, 5, 30);
}

void loop()  {
  pwmled.update();   
}


