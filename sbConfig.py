import os
import pickle
import glob
from sbProfile import sbProfile
import sbProfileExporter as sbPE
import sbCalculator as sbCalc


def createNewProfile(selection):

    name = ''
    while not name:
        name = input("> Profile Name: ").strip()

    profile = sbProfile(name)
    profile.tireDiameter = parseNumericInput("> Tire Diameter (in): ", 'float')
    profile.gearCount = parseNumericInput("> Gear Count: ", 'int')
    for i in range(0, profile.gearCount):
        valid = False
        while not valid:
            ratio = parseNumericInput("> [Gear " + str(i+1) + "] Overall Ratio: ", 'float')
            if i >= 1 and ratio >= profile.gearRatios[i-1]:
                print("Error: Input a gear ratio smaller than the previous")
            else: valid = True
        profile.gearRatios.append(ratio)


    if selection == 1:
        for i in range(0, profile.gearCount):
            profile.shiftPoints.append(parseNumericInput("> [Gear " + str(i+1) +"] Shift Point (RPM): ", 'float'))
    elif selection == 2:

        minRPM = parseNumericInput("""\n[ Beginning Torque Curve Analysis  ]
                                   \n> Please enter your vehicle's minimum idle RPM (Generally about 1000)
                                   \n> Min RPM: """, 'float')

        maxRPM = parseNumericInput("""\n> Now enter your vehicle's maximum RPM (redline RPM)
                                   \n> Max RPM: """, 'float')

        clear()
        print("[ Please enter torque values for the given RPMs ]")
        definingPoints = []
        rpm = minRPM

        done = False
        while not done:
            if rpm >= maxRPM:
                rpm = maxRPM
                done = True  
            tq = parseNumericInput("> [ " + str(rpm)  +" RPM ] Torque: ", 'float')
            definingPoints.append((rpm,tq))
            rpm += 500.0


        profile.shiftPoints = sbCalc.calculateShiftPoints(profile.gearRatios, definingPoints)
        print("\n")


    else: assert(False)

    profile.earlyWarning = parseNumericInput("> Early Warning (RPM): ", 'float')
    clear()

    profile.summary()

    if profile.isGood():  save(profile, "\n> Output Directory: ")
    else: assert(False)
    clear()
    print("[ SB Profile has been saved ]\n\n")











def createNewProfileMenu():
    createMenu = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|     Profile Creation Menu      |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| 1. Create manually             |
| 2. Create with TQ Curve        |
| 0. Main Menu                   |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    options = {0 : lambda x: None,
               1 : createNewProfile,
               2 : createNewProfile,
    }

    selection = getMenuOption(createMenu, options)
    options[selection](selection)
    return selection









def exportProfilesMenu():
    print("[ Export Profiles ]")
    # input filepath
    # if files don't exist, fight back and say they don't exist probably?
    # while loop until user hits 0, adding files to list so long as they don't exist already
    # if the list isn't empty (which it shouldn't be)
    # prompt the doofus for a export filepath
    # Export
    profiles = []
    path = ''
    #should be if this is true....
    sbPE.export(profiles, path)
    print ("File export succesful")
    return










def getMenuOption(menu, options):
    menu = menu + "\n> Please select a menu option: "

    valid = False
    while not valid:
        try:
            selection = parseNumericInput(menu, 'int')
            if selection in options:
                valid = True
            else: print("\nInvalid selection\n")
        except:
            print("\nInvalid selection\n")
            continue
    clear()
    return selection











def parseNumericInput(prompt = '', dataType = 'int'):
    dataTypes = {'int' : lambda x: int(x),
                 'float' : lambda x: float(x),
    }
    assert(dataType in dataTypes)

    valid = False
    while not valid:
         try:
             userInput = dataTypes[dataType](input(prompt).strip())
             valid = True
         except ValueError:
             print("\nInvalid Input: Please enter a value of type " + dataType + "\n")
             continue
    return userInput












def save(profile, prompt = '', path = None):
    saved = False
    while not saved:
        try:
            if path == None:
                filepath = os.path.abspath(os.path.normpath(input(prompt).strip()))
            else: filepath = path
            if not os.path.isdir(filepath):
                print("File Directory not found. Attempting to create.")
                os.makedirs(filepath)
            with open(os.path.join(filepath, profile.name + '.sb'), 'wb') as sbFile:
                pickle.dump(profile, sbFile, 2)
                sbFile.close()
            saved = True
        except Exception:
            print("\nInvalid path or permission issue. Attempt saving to a different directory")
            if path == None: continue
            assert(False)












def viewProfiles(selection):
    clear()
    if selection == 1:
        profile = load("> Input Profile Path: ")
        clear()
        profile.summary()
        return getMenuOption("\n> 0. Back",[0])

    elif selection == 2:
        found = False
        while not found:
            profileDirectory = os.path.abspath(os.path.normpath(input("> Input Profile Directory: ")))
            if not os.path.isdir(profileDirectory):
                print("File directory not found")
                continue
            else:
                found = True
                clear()

        sbFiles = glob.glob(os.path.join(profileDirectory, '*.sb'))
        sbFileMenu = "[ Shift Buddy Files ]\n"
        for i in range(0, len(sbFiles)):
            (tmp, fileName) = os.path.split(sbFiles[i])
            sbFileMenu += (str(i+1) + ". " + fileName + "\n")
        sbFileMenu += "0. Main Menu\n"

        options = list(range(len(sbFiles)+1))
        selection = int(getMenuOption(sbFileMenu, options)) - 1
        while selection != -1:
            profile = load(path=sbFiles[selection])
            clear()
            profile.summary()
            getMenuOption("\n> 0. Back", [0])
            selection = int(getMenuOption(sbFileMenu, options)) - 1








def load(prompt = '', path = None):
    loaded = False
    profile = None
    while not loaded:
        if path == None:
            filepath =  os.path.abspath(os.path.normpath(input(prompt).strip()))
        else: filepath = path
        try:
            with open(filepath, 'rb') as sbFile:
                profile = pickle.load(sbFile)
                sbFile.close()
            loaded=True
        except Exception:
            print("\nInvalid path or permission issue. Double check input file or folder path")
            if path == None: continue
            assert(False)
        return profile










def viewProfilesMenu():
    viewMenu = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|         View Profiles          |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| 1. Profile Path                |
| 2. Profile Directory           |
| 0. Main Menu                   |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    options = {0 : lambda x: None,
               1 : viewProfiles,
               2 : viewProfiles,
    }
    selection = getMenuOption(viewMenu, options)
    options[selection](selection)
    return selection












def mainMenu():
    mainMenu = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|           Main Menu            |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| 1. Create new profile          |
| 2. Export existing profiles    |
| 3. View existing profiles      |
| 0. Exit                        |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    options = {0 : lambda: None,
               1 : createNewProfileMenu,
               2 : exportProfilesMenu,
               3 : viewProfilesMenu,
    }

    selection = getMenuOption(mainMenu,options)
    options[selection]()
    return selection










def clear():
    os.system('cls' if os.name == 'nt' else 'clear')







def main():
    clear()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("| Shift Buddy Configuration Tool |")

    option = mainMenu()
    while (option != 0):
        option = mainMenu()






if __name__ == "__main__":
    main()
