#include <OBD.h>
#include <TM1638.h>
#include "ProfileManager.h"
#include "ButtonPIDs.h"

/* Freematics OBD-II Adapter / Pre-Init */
COBDI2C obd;
int currentSpeedKPH = 0;
int currentRPM = 0;
int currentPIDData = 0;
byte currentPID = BTN2_PID;

/* TM-1638 Display / Pre-Init */
TM1638 module(8,9,10, true, 7);
#define GREEN 1
#define GREEN_LEDS 3
#define RED 2
#define RED_LEDS 2
#define ORANGE 3
#define ORANGE_LEDS 3
#define LED_COUNT 8
byte PIDButton = 0;
byte lastPIDButton = 0;
word ledIncFactor = 0;
byte ledLightCount = 0;

/* ShiftBuddy Profile Manager / Pre-Init */
ProfileManager sbProfileManager;
word currentShiftPoint = 0;


void setup()
{
  obd.begin();
  while (!obd.init());
  while (!sbProfileManager.init());
}


void updateLEDs(const int& shiftRPM)
{
  ledIncFactor = shiftRPM/LED_COUNT;
  ledLightCount = currentRPM/ledIncFactor;
  
  for (byte i = 0; i < LED_COUNT; ++i)
  {
    if (i <= ledLightCount)
    {
      if (i<GREEN_LEDS)
        module.setLED(GREEN, i);
      else if (i >= GREEN_LEDS && i < ORANGE_LEDS)
        module.setLED(ORANGE, i);
      else
        module.setLED(RED, i);
    }
    else
    {
      module.setLED(0, i);
    }
  }
}



void updateNumericDisplay(const int& data)
{
  module.setDisplayToDecNumber(data, 0, false);
}



void notify(const String& message,const unsigned int& duration)
{
  module.clearDisplay();
  module.setLEDs(0);
  module.setDisplayToString(message);
  delay(duration);
}


void signalUpshift(const String& message, const unsigned int& duration)
{
  module.clearDisplay();
  module.setLEDs(0x00);
  delay(duration);
  module.setLEDs(0xFF << 8);
  module.setDisplayToString(message);
  delay(duration);
}


void buttonLogic(const byte& buttons)
{
  
  if ((int)buttons > 0)
  {
    if (buttons != lastPIDButton)
    {
      switch((int)buttons)
      {
        case 1:
          notify(sbProfileManager.nextProfile(), 1000);
          return;
        case 2:
          currentPID = BTN2_PID;
          break;
        case 4:
          currentPID = BTN3_PID;
          break;
        case 8:
          currentPID = BTN4_PID;
          break;
        case 16:
          currentPID = BTN5_PID;
          break;
        case 32:
          currentPID = BTN6_PID;
          break;
        case 64:
          currentPID = BTN7_PID;
          break;
        case 128:
          currentPID = BTN8_PID;
          break;
      }
      notify("PID - "+String(currentPID, HEX), 1000);
      lastPIDButton = buttons;
    }
  }
}



void loop()
{
  buttonLogic(module.getButtons());
  
  obd.read(PID_SPEED, currentSpeedKPH);
  obd.read(PID_RPM, currentRPM);
  obd.read(currentPID, currentPIDData);
  
  currentShiftPoint = sbProfileManager.getShiftPoint(currentSpeedKPH, currentRPM);
  if (currentRPM < currentShiftPoint)
  {
    updateNumericDisplay(currentPIDData);
    updateLEDs(currentShiftPoint);
  }
  else
    signalUpshift("GEAR UP", 75); 
}
