# Author: mbichay@github
#
# Description: Translates sbProfile object values into string form
# in order to generate a ProfileManager header file to be uploaded
# to the Arduino. (Export)

# ProfileManager.h
ProfileManagerDotH = """\
#include <Arduino.h>
#ifndef PROFILEMANAGER_H
#define PROFILEMANAGER_H
#define PROFILE_COUNT {PROFILE_COUNT}
#define MAX_GEARS {MAX_GEARS}

class ProfileManager
{{
public:
ProfileManager();
bool init();
const String nextProfile();
const float getShiftPoint(int& currentSpeedKPH, int& currentRPM) const;
const byte currentGearModel(int& currentSpeedKPH, int& currentRPM) const;
private:
byte currentProfile = -1;
const String profileName[PROFILE_COUNT] = {PROFILE_NAME};
const float tireDiameter[PROFILE_COUNT] = {TIRE_DIAMETER};
const byte gearCount[PROFILE_COUNT] = {GEAR_COUNT};
const float gearRatios[PROFILE_COUNT][MAX_GEARS] = {GEAR_RATIOS};
const float shiftPoints[PROFILE_COUNT][MAX_GEARS] = {SHIFT_POINTS};
const float earlyWarning[PROFILE_COUNT] = {EARLY_WARNING};
}};
#endif
"""



# Main callable function from this file, takes an input of a list of sbProfiles
# and converts the numeric values to strings, then formats them to the header template above
def generateProfileManagerHeader(sbProfiles):
    
    profileCount = len(sbProfiles)
    profileName = []
    tireDiameter = []
    gearCount = []
    gearRatios = []
    shiftPoints = []
    earlyWarning = []
    
    # Pull all data from sbProfiles and append to seperate lists
    for profile in sbProfiles:
        profileName.append(profile.name)
        tireDiameter.append(profile.tireDiameter)
        gearCount.append(profile.gearCount)
        gearRatios.append(profile.gearRatios)
        shiftPoints.append(profile.shiftPoints)
        earlyWarning.append(profile.earlyWarning)

    # Find the max amount of gears out of any of the profiles in order to
    # back fill the rest of the values with -1s (Convenience for initializing C arrays)
    maxGears = max(gearCount)
    normalize(gearRatios, -1, maxGears)
    normalize(shiftPoints, -1, maxGears)

    # Append string data to formatted header file.
    global ProfileManagerDotH
    formattedProfileManagerDotH = ProfileManagerDotH.format(
            PROFILE_COUNT = profileCount
            ,MAX_GEARS = maxGears
            ,PROFILE_NAME = cppBrackets(str(profileName))
            ,TIRE_DIAMETER = cppBrackets(str(tireDiameter))
            ,GEAR_COUNT = cppBrackets(str(gearCount))
            ,GEAR_RATIOS = cppBrackets(str(gearRatios))
            ,SHIFT_POINTS = cppBrackets(str(shiftPoints))
            ,EARLY_WARNING = cppBrackets(str(earlyWarning))
            )
    
    # return the header file in string format.
    return formattedProfileManagerDotH

# Adds a value to the end of a list in order for it to meet a required length
def normalize(lists ,value , length):

    for list in lists:
        for i in range(len(list), length):
            list.append(value)
    return lists

# Swaps brackets into curly braces in a string. Used for intializing C arrays.
def cppBrackets(string):
    return string.replace('[','{').replace(']','}').replace('\'', '\"')
        
