


ProfileManagerDotH = """\
#ifndef PROFILEMANAGER_H
#define PROFILEMANAGER_H
#define PROFILE_COUNT {profileCount}
#define MAX_GEARS {maxGears}

class ProfileManager {
public:
ProfileManager();
bool init();
const String nextProfile();
const float getShiftPoint(int& currentSpeedKPH, int& currentRPM) const;
const byte currentGearModel(int& currentSpeedKPH, int& currentRPM) const;
private:
byte currentProfile = -1;
const String profileName[PROFILE_COUNT] = {profileName};
const float tireDiameter[PROFILE_COUNT] = {tireDiameter};
const byte gearCount[PROFILE_COUNT] = {gearCount};
const float gearRatios[PROFILE_COUNT][MAX_GEARS] = {gearRatios};
const float shiftPoints[PROFILE_COUNT][MAX_GEARS] = {shiftPoints};
const word earlyWarning[PROFILE_COUNT] = {earlyWarning};
};
#endif
"""




def generateProfileManagerHeader(sbProfiles):
    return 0
