#include <arduino.h>
#include "ProfileManager.h"

#define KPH_TO_IPM 656.168


ProfileManager::ProfileManager()
{
  
}

bool ProfileManager::init()
{
  if (PROFILE_COUNT <= 0)
    return false;
  nextProfile();
  return true;
}

String ProfileManager::nextProfile()
{
  ++currentProfile;
  if (currentProfile >= PROFILE_COUNT)
  {
    currentProfile = 0;
  }
  return profileName[currentProfile];
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

