#ifndef PROFILEMANAGER_H
#define PROFILEMANAGER_H
#define PROFILE_COUNT 2
#define MAX_GEARS 10

class ProfileManager {
  public:
    ProfileManager();
    bool init();
    const String nextProfile();
    const float getShiftPoint(int& currentSpeedKPH, int& currentRPM) const;
    const byte currentGearModel(int& currentSpeedKPH, int& currentRPM) const;
  private:
    byte currentProfile = -1;
    const String profileName[PROFILE_COUNT] = {"Golf R", "BMW M3"};
    const float tireDiameter[PROFILE_COUNT] = {27.32, 27.32};
    const byte gearCount[PROFILE_COUNT] = { 6, 5};
    const float gearRatios[PROFILE_COUNT][MAX_GEARS] = { {13.93, 8.73, 6.25, 4.63, 3.58, 2.79, -1, -1, -1, -1},
                                                   {13.93, 8.73, 6.25, 4.63, 3.58, -1, -1, -1, -1, -1}};
    const float shiftPoints[PROFILE_COUNT][MAX_GEARS] = { { 6500, 6500, 6500, 6500, 6500, 6500 },
                                                    { 5500, 5500, 5500, 5500, 5500, 5500 } };
    const word earlyWarning[PROFILE_COUNT] = { 500, 500 };
};

#endif
