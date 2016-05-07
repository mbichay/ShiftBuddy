#include <TM1638.h>

#define LED_COUNT 8
#define BTN_COUNT 8

class DisplayController
{
  public:
    DisplayController() : module(8,9,10, true, 7) {}
    void updateShiftMeter(unsigned int currentRPM, unsigned int shiftRPM);
    void signalUpshift(unsigned int delay, String message);

  private:
    /* TODO */
    TM1638 module;
};

