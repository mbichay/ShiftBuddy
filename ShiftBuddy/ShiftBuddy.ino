/* Author: mbichay@github
 *
 * Description: Main control logic for the Shift Buddy shift-light.
 * Code was made modular for the purpose of being modifiable, things like
 * how the shift light communicates to you as well as what it displays is fully
 * customizable. Feel free to make any modifications.
*/

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


/* Updates the LEDs to act as a meter gauging how close you are to the next shift point */
void updateLEDs(const int& shiftRPM)
{
  /* Incremental factor for updating each light in order. */
  ledIncFactor = shiftRPM/LED_COUNT;
  ledLightCount = currentRPM/ledIncFactor;
  
  /* Serially turning on and off LEDs based on how many increments the current RPM has passed */
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


/* Defaults set for displaying numeric data. Ignores leading zeros */
void updateNumericDisplay(const int& data)
{
  module.setDisplayToDecNumber(data, 0, false);
}


/* Notifies the user of any message input into the function for a set duration. */
void notify(const String& message,const unsigned int& duration)
{
  /* Clear LEDs and print string to display */
  module.clearDisplay();
  module.setLEDs(0);
  module.setDisplayToString(message);
  delay(duration);
}


/* Logic for how the upshift signals to the user. Easily modifiable to meet your likings */
void signalUpshift(const String& message, const unsigned int& duration)
{
  /* Flash LEDS red and display input message. */
  module.clearDisplay();
  module.setLEDs(0x00);
  delay(duration);
  module.setLEDs(0xFF << 8);
  module.setDisplayToString(message);
  delay(duration);
}


void buttonLogic(const byte& buttons)
{
  /* If at least one button is pressed. */
  if ((int)buttons > 0)
  {
    /* If the button isn't a repeat-press for a PID button */
    if (buttons != lastPIDButton)
    {
      switch((int)buttons)
      {
        /* First button triggers profile switch */
        case 1:
          notify(sbProfileManager.nextProfile(), 1000);
          return;
        /* Otherwise, switch the PID based on pre-defined button-PID mappings */
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
      /* Display to the user the selected PID in HEX */
      notify("PID - " + String(currentPID, HEX), 1000);
      lastPIDButton = buttons;
    }
  }
}


void setup()
{
  /* Establish connection to the OBDII bus. */
  obd.begin();
  while (!obd.init());

  /* Initialize the profile database and manager */
  while (!sbProfileManager.init());
}


void loop()
{
  /* Check for the profile-switching button and update user-requested PID */
  buttonLogic(module.getButtons());
  
  /* Poll ECU for speed and RPM for calculating the current gear */ 
  obd.read(PID_SPEED, currentSpeedKPH);
  obd.read(PID_RPM, currentRPM);

  /* Poll ECU for the user-requested PID */
  obd.read(currentPID, currentPIDData);
  
  /* If the current RPM is less than the calculated shift Point */
  currentShiftPoint = sbProfileManager.getShiftPoint(currentSpeedKPH, currentRPM);
  if (currentRPM < currentShiftPoint)
  {
    /* Update the LEDs to the user, update the user-requested PID to the user */
    updateNumericDisplay(currentPIDData);
    updateLEDs(currentShiftPoint);
  }
  /* otherwise tell the user to up-shift! */
  else
  {
    signalUpshift("GEAR UP", 75); 
  }
}
