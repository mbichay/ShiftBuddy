
#define PROFILE_COUNT 1
#define MAX_GEARS 10

class ProfileManager {
  public:
    ProfileManager();
    bool init(short profileNumber);
    bool switchProfile(short profileNumber);
    unsigned int getShiftPoint(float currentSpeedKPH, int currentRPM);
    unsigned int currentGearModel(float currentSpeedKPH, int currentRPM);
  private:
    short currentProfile = -1;
    float tireDiameter[PROFILE_COUNT] = {27.32};
    short gearCount[PROFILE_COUNT] = { 6 };
    float gearRatios[PROFILE_COUNT][MAX_GEARS] = { {13.93, 8.73, 6.25, 4.63, 3.58, 2.79, -1, -1, -1, -1} };
    float shiftPoints[PROFILE_COUNT][MAX_GEARS] = { { 6500, 6500, 6500, 6500, 6500, 6500 } };
    unsigned int earlyWarning[PROFILE_COUNT] = { 500 };
};

