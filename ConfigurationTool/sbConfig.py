# Author: mbichay@github
#
# Description: This is the main runnable command line application for configuring
# the shift buddy. All profile creation and export can be done through this tool or
# effectively by hand if one were to want to circumvent this CLI.

import os
import pickle
import glob
from sbProfile import sbProfile
import sbProfileExporter as sbPE
import sbCalculator as sbCalc


# Create new profile logic
# Allows for manual input of your own profile values as well as autogenerating
# optimum shift points based on legrange and linear interpolation
def createNewProfile(selection):

    # The following is required for manual and auto-generated input:
    # Parse profile name
    name = ''
    while not name:
        name = input("> Profile Name: ").strip()
    profile = sbProfile(name)

    # Parse tire diameter
    profile.tireDiameter = parseNumericInput("> Tire Diameter (in): ", 'float')

    #Parse gear count
    profile.gearCount = parseNumericInput("> Gear Count: ", 'int')

    # Parse all overall gear ratios (gear ratio * final gear ratio)
    for i in range(0, profile.gearCount):
        valid = False
        while not valid:
            ratio = parseNumericInput("> [Gear " + str(i+1) + "] Overall Ratio: ", 'float')
            if i >= 1 and ratio >= profile.gearRatios[i-1]:
                print("Error: Input a gear ratio smaller than the previous")
            else: valid = True
        profile.gearRatios.append(ratio)

    # If the user is going to enter shift points in manually,
    # parse all of the shift points for each gear
    if selection == 1:
        for i in range(0, profile.gearCount):
            profile.shiftPoints.append(parseNumericInput("> [Gear " + str(i+1) +"] Shift Point (RPM): ", 'float'))

    # Else if the user is going to use the shift point calculator
    elif selection == 2:
        
        # Request if they want to try legrange or linear interpolation
        menu = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| Beginning Torque Curve Analysis |
| > Choose interpolation schema < |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| 1. legrange                     |
| 2. linear                       |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
        options = {1 : "legrange",
                   2 : "linear"
        }
        interpolationType = getMenuOption(menu, options)

        # Pull the min and maximum (redline) RPM values
        minRPM = parseNumericInput("""\n> Please enter your vehicle's minimum idle RPM (Generally about 1000) 
                                      \n> Min RPM: """, 'float')

        maxRPM = parseNumericInput("""\n> Now enter your vehicle's maximum RPM (redline RPM)
                                      \n> Max RPM: """, 'float')

        # Enter in "Defining points" about the torque curve, torque information at every 500rpm interval from min to max
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

        # Calculate optimum shift points
        profile.shiftPoints = sbCalc.calculateShiftPoints(profile.gearRatios, definingPoints, interpolationType)
        print("\n")


    else: assert(False)

    # This is required for mnanual or auto-generated shift points
    profile.earlyWarning = parseNumericInput("> Early Warning (RPM): ", 'float')
    clear()

    # print the summary of the newly created profile
    profile.summary()

    # If the profile was created succesfully, parse an output directory and save the Pickle file of the sbProfile object
    if profile.isGood():  save(profile, "\n> Output Directory: ")
    else: assert(False)
    clear()
    print("[ SB Profile has been saved ]\n\n")




# Create new profile menu selection and execution page
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



# Export logic for exporting selected sbProfiles into a ProfileManager.h C/Arduino header
def exportProfilesMenu():

    print("[ Export Profiles ]")
    profileDirectory = parseFileDirectoryInput("> Input Profile Directory: ", False)
    sbFiles = glob.glob(os.path.join(profileDirectory, '*.sb'))
    selectedProfilePaths = []
    selectedProfileNames = []
    
    # While the user hasn't selected the 0 option. for export
    done = False
    while not done:
        sbProfileExportList = "[ Add Profiles to Export List ]\n"
        for i in range(0, len(sbFiles)):
            (tmp, fileName) = os.path.split(sbFiles[i])
            sbProfileExportList += (str(i+1) + ". " + fileName + "\n")
        sbProfileExportList += "\n> Selected Profiles: " + str(selectedProfileNames)  + "\n"
        sbProfileExportList += "\n0. Finish export\n"
        
        options = list(range(len(sbFiles)+1))
        selection = int(getMenuOption(sbProfileExportList, options)) - 1
        
        if selection == -1:
            done = True
        else:
            # Add selected profiles to a list (one list for outputting to the user,
            # and one full-filepath list for loading the objects)
            selectedProfilePaths.append(sbFiles[selection])
            (tmp, fileName) = os.path.split(sbFiles[selection])
            selectedProfileNames.append(fileName)
            sbFiles.remove(sbFiles[selection])
    
    # Load all sbProfile objects
    clear()
    sbProfiles = []
    for filepath in selectedProfilePaths:
        sbProfiles.append(load(None, filepath))

    # Parse export directory for exporting the header file
    exportDirectory = parseFileDirectoryInput("[ Enter ShiftBuddy Directory (Path containing Arduino Files) ]\n> Input ShiftBuddy Folder Path: ", False)

    try: 
        with open(os.path.join(exportDirectory, 'ProfileManager.h'), 'w+') as profileManagerDotH:
            # Retrieve the ProfileManager.h in a multi-line string and output to a file.
            profileManagerDotH.write(sbPE.generateProfileManagerHeader(sbProfiles))

    except Exception:
        print("File permissions issue. Cannot write file to specified directory.")
        assert(False)
    clear()
    print("Export Succesful. You may now upload the ShiftBuddy files to the Arduino.")
    return


# Parses and cleans filepath/directory input from user
# If tryToCreate flag is True, it will attempt to create that directory
def parseFileDirectoryInput(prompt, tryToCreate):
    found = False
    while not found:
        directory = os.path.abspath(os.path.normpath(input(prompt).strip()))
        if not os.path.isdir(directory):
            print("File directory not found")
            if tryToCreate:
                print("File Directory not found. Attempting to create.")
                os.path.makedirs(directory)
            continue
        else:
            found = True
            clear()
    return directory



# Pass the user a menu prompt and a list of options
# If the user input is within the list of options, returns the selection
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


# Convenience function for converting user input into numeric datatype
# Only supports int and float
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



# Saves the sbProfile object into a binary pickle file
# If a prompt is given, requests a path for saving the file
# If a path is given, skips prompt and proceeds to save
def save(profile, prompt = '', path = None):
    saved = False
    while not saved:
        try:
            if path == None:
                filepath = parseFileDirectoryInput(prompt, True)
            else: filepath = path
            with open(os.path.join(filepath, profile.name + '.sb'), 'wb') as sbFile:
                pickle.dump(profile, sbFile, 2)
                sbFile.close()
            saved = True
        except Exception:
            print("\nInvalid path or permission issue. Attempt saving to a different directory")
            if path == None: continue
            assert(False)



# View Profiles feature allows the user to see the information stored within an SB File(s)
def viewProfiles(selection):
    clear()

    # If the user wants to look at a specific file, selection will be 1
    if selection == 1:
        profile = load("> Input Profile Path: ")
        clear()
        profile.summary()
        return getMenuOption("\n> 0. Back",[0])

    # Otherwise, if a user wants to look at a collection of files in a directory, the selection will be 2
    elif selection == 2:
        profileDirectory = parseFileDirectoryInput("> Input Profile Directory: ", False)
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



# Given a prompt, asks the user for a path to a SB File. Given a path, skips the prompt.
# Loads the SB file into a sbProfile object
def load(prompt = '', path = None):
    loaded = False
    profile = None
    while not loaded:
        # If a path isn't given
        if path == None:
            filepath =  os.path.abspath(os.path.normpath(input(prompt).strip()))
        else: filepath = path
        try:
            # Open as a binary/read
            with open(filepath, 'rb') as sbFile:
                profile = pickle.load(sbFile)
                sbFile.close()
            loaded=True
        except Exception:
            print("\nInvalid path or permission issue. Double check input file or folder path")
            if path == None: continue
            assert(False)
        return profile



# Profile menu selection and execution page
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


# Main menu selection and execution page
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


# Clears all text from the terminal.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Command-Line interface's While(1) Loop.
def main():
    clear()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("| Shift Buddy Configuration Tool |")

    option = mainMenu()
    while (option != 0):
        option = mainMenu()


if __name__ == "__main__":
    main()
