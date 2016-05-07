#include "DisplayController.h"


void DisplayController::updateShiftMeter(unsigned int currentRPM, unsigned int shiftRPM)
{
  unsigned int factor = shiftRPM/LED_COUNT;
  unsigned int LEDS = currentRPM/factor;
  short color;

  module.setDisplayToDecNumber(currentRPM, 0, false);


  for (int i = 0; i < LED_COUNT; ++i)
  {
    color = 0;
    if (i <= LEDS)
    {
      if (i<3)
        color = 1;
      else if (i >= 3 && i < 6)
        color = 3;
      else
        color = 2;
      module.setLED(color, i);
    }
    else
    {
      module.setLED(color, i);
    }
  }
}


void DisplayController::signalUpshift(unsigned int duration, String message)
{
  module.clearDisplay();
  module.setLEDs(0x00);
  delay(duration);
  module.setLEDs(0xFF << 8);
  module.setDisplayToString(message);
  delay(duration);
}

