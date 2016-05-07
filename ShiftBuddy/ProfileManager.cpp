#include <arduino.h>
#include "ProfileManager.h"

#define KPH_TO_IPM 656.168


ProfileManager::ProfileManager()
{
  
}

bool ProfileManager::init(short profileNumber)
{
  if (switchProfile(profileNumber) == 1)
    return true;
  return false;
}

bool ProfileManager::switchProfile(short profileNumber)
{
  if (profileNumber < PROFILE_COUNT)
  {
    currentProfile = profileNumber;
    return true;
  }
  return false;
}

unsigned int ProfileManager::currentGearModel(float currentSpeedKPH, int currentRPM)
{
  unsigned int currentGear = 1;
  
  if (currentRPM > 0 && currentSpeedKPH == 0)
    return currentGear;

  float ratio = ((PI * tireDiameter[currentProfile]) / (currentSpeedKPH * KPH_TO_IPM) * currentRPM);

  
  float min = abs(ratio - gearRatios[currentProfile][0]);
  float diff;
  for (int gearIdx = 1; gearIdx < gearCount[currentProfile]; ++gearIdx)
  {
    diff = abs(ratio - gearRatios[currentProfile][gearIdx]);
    if (diff <= min)
    {
      min = diff;
      currentGear = gearIdx+1;
    }
  }
  return currentGear;
}

unsigned int ProfileManager::getShiftPoint(float currentSpeedKPH, int currentRPM)
{
  return shiftPoints[currentProfile][currentGearModel(currentSpeedKPH, currentRPM)-1] - earlyWarning[currentProfile];
}

