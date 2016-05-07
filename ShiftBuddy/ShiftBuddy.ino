
#include "DisplayController.h"
#include "ProfileManager.h"
#include <OBD.h>

COBDI2C obd;
ProfileManager sbProfileManager;
DisplayController sbDisplayController;
int currentSpeedKPH = 0;
int currentRPM = 0;
int currentShiftPoint = 0;

void setup() {
  // put your setup code here, to run once:
  obd.begin();
  while (!obd.init());
  while (!sbProfileManager.init(0));
}

void loop() {
  // put your main code here, to run repeatedly:
  obd.read(PID_SPEED, currentSpeedKPH);
  obd.read(PID_RPM, currentRPM);
  currentShiftPoint = sbProfileManager.getShiftPoint(currentSpeedKPH, currentRPM);
  if (currentRPM < currentShiftPoint)
    sbDisplayController.updateShiftMeter(currentRPM,currentShiftPoint);
  else
    sbDisplayController.signalUpshift(100,"GEAR UP"); 
}
