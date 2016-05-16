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

const String ProfileManager::nextProfile()
{
  ++currentProfile;
  if (currentProfile >= PROFILE_COUNT)
  {
    currentProfile = 0;
  }
  return profileName[currentProfile];
}


const byte ProfileManager::currentGearModel(int& currentSpeedKPH, int& currentRPM) const
{
  byte currentGear = 1;
  if (currentRPM > 0 && currentSpeedKPH == 0)
    return currentGear;

  float ratio = ((PI * tireDiameter[currentProfile]) / ((float)currentSpeedKPH * KPH_TO_IPM) * (float)currentRPM);
  
  float min = abs(ratio - gearRatios[currentProfile][0]);
  float diff;
  for (byte gearIdx = 1; gearIdx < gearCount[currentProfile]; ++gearIdx)
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

const float ProfileManager::getShiftPoint(int& currentSpeedKPH, int& currentRPM) const
{
  return shiftPoints[currentProfile][currentGearModel(currentSpeedKPH, currentRPM)-1] - earlyWarning[currentProfile];
}

