#include <OBD.h>
#include <TM1638.h>
#include "ProfileManager.h"
#include "ButtonPIDs.h"

/* Freematics OBD-II Adapter / Pre-Init */
COBDI2C obd;
int currentSpeedKPH = 0;
int currentRPM = 0;
int currentPID = BTN2_PID;
int currentPIDData = 0;
int readArray[3] = {};
byte pidArray[3] = {PID_RPM, PID_SPEED, PID_RPM};

/* TM-1638 Display / Pre-Init */
TM1638 module(8,9,10, true, 7);
#define LED_COUNT 8
#define BTN_COUNT 8
#define GREEN 1
#define RED 2
#define ORANGE 3

byte profileButton = 0;
byte lastProfileButton = 0;

byte PIDButton = 0;
byte lastPIDButton = 0;

/* ShiftBuddy Profile Manager / Pre-Init */
ProfileManager sbProfileManager;
int currentShiftPoint = 0;


int counter = 0;


void setup()
{
  obd.begin();
  while (!obd.init());
  while (!sbProfileManager.init());
}


void updateLEDs(int shiftRPM)
{
  unsigned int factor = shiftRPM/LED_COUNT;
  unsigned int LEDS = currentRPM/factor;
  
  for (int i = 0; i < LED_COUNT; ++i)
  {
    if (i <= LEDS)
    {
      if (i<3)
        module.setLED(GREEN, i);
      else if (i >= 3 && i < 6)
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

void updateNumericDisplay(int data)
{
  module.setDisplayToDecNumber(counter, 0, false);
}


bool profileButtonPressed()
{
  bool pressed = false;
  profileButton = module.getButtons();
  if (profileButton != lastProfileButton)
  {
    if ((int)profileButton == 1)
    {
      pressed = true;
    }
  }
  lastProfileButton = profileButton;
}


void notify(String message,unsigned int duration)
{
  module.clearDisplay();
  module.setLEDs(0);
  module.setDisplayToString(message);
  delay(duration);
}


void signalUpshift(String message, unsigned int duration)
{
  module.clearDisplay();
  module.setLEDs(0x00);
  delay(duration);
  module.setLEDs(0xFF << 8);
  module.setDisplayToString(message);
  delay(duration);
}


bool test()
{
  bool pressed=false;
  PIDButton = module.getButtons();
  if (PIDButton != lastPIDButton)
  {
    if ((int)PIDButton == 2)
    {
      pressed=true;
    }
  }
  lastPIDButton = PIDButton;
  return pressed;
}

void buttonLogic()
{
  byte button = module.getButtons();

  if ((int)button > 0)
  {
    if ((int)button == 1)
    {
      if (button != lastProfileButton)
        notify(sbProfileManager.nextProfile(), 1000);
      lastProfileButton = button;
    }
    else
    {
      if (button != lastPIDButton)
      {
        switch((int)button)
        {
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
        notify(String(currentPID), 1000);
        lastPIDButton = button;
      }
    }
    delay(10);
    lastProfileButton = 0;
  }
}



void loop()
{
  buttonLogic();
  ++counter;
  /*
  obd.read(PID_SPEED, currentSpeedKPH);
  obd.read(PID_RPM, currentRPM);
  obd.read(currentPID, currentPIDData);
*/
  obd.read(pidArray, 3, readArray);
  
  currentShiftPoint = sbProfileManager.getShiftPoint(currentSpeedKPH, currentRPM);
  if (currentRPM < currentShiftPoint)
  {
    updateNumericDisplay(currentPIDData);
    updateLEDs(currentShiftPoint);
  }
  else
    signalUpshift("GEAR UP", 75); 
}
