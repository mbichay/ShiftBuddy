# Author: mbichay@github
#
# Description: Profile object for holding all data and metadata
# about a specific vehicle's profile and characteristics

class sbProfile(object):
    def __init__(self, name=''):
        self.name = name
        self.tireDiameter = -1
        self.gearCount = -1
        self.gearRatios = []
        self.shiftPoints = []
        self.earlyWarning = -1

    def isGood(self):
        if (self.name != '' and
            self.tireDiameter != -1 and
            self.gearCount != -1 and
            self.earlyWarning != -1 and
            len(self.gearRatios) == self.gearCount and
            len(self.shiftPoints) == self.gearCount
            ):
            return True
        return False

    def summary(self):
        print("[ Profile Summary ]")
        print("Name: " + self.name)
        print("Tire Diameter (in): " + str(self.tireDiameter))
        print("Gear Count: " + str(self.gearCount))
        print("Gear Ratios: " + str(self.gearRatios))
        print("Shift Points (RPM): " + str(self.shiftPoints))
        print("Early Warning (RPM): " + str(self.earlyWarning))


if __name__ == "__main__":
    pass
