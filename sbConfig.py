import os
import pickle
from sbProfile import sbProfile


def createNewProfile(selection):
     
    profile = sbProfile(input("> Profile Name: "))
    profile.tireDiameter = parseNumericInput("> Tire Diameter (in): ", 'float')
    profile.gearCount = parseNumericInput("> Gear Count: ", 'int')
    for i in range(0, profile.gearCount):
        profile.gearRatios.append(parseNumericInput("> [Gear " + str(i+1) + "] Overall Ratio: ", 'float'))
   
    if selection == '1':
        for i in range(0, profile.gearCount): 
            profile.shiftPoints.append(parseNumericInput("> [Gear " + str(i+1) +"] Shift Point (RPM): ", 'float'))
    else:
        pass

    profile.earlyWarning = parseNumericInput("> Early Warning (RPM): ", 'float')
    clear()

    profile.summary()
    
    path = os.path.abspath(os.path.normpath(input("\n> Output Directory: ")))
    if profile.isGood():  save(profile, path)
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
| 0. Back                        |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    options = {'0' : lambda x: None,
               '1' : createNewProfile,
               '2' : createNewProfile,
    }
    
    selection = getMenuOption(createMenu, options)
    options[selection](selection)
    return selection


def exportProfilesMenu():
    return 0


def getMenuOption(menu, options):
    menu = menu + "\n> Please select a menu option: " 
    selection = input(menu)
    while selection not in options:
        print("\nInvalid selection\n")
        selection = input(menu)
    clear()
    return selection


def parseNumericInput(prompt, dataType = 'int'):
    
    dataTypes = {'int' : lambda x: int(x),
                 'float' : lambda x: float(x),
    }
    assert(dataType in dataTypes)
    
    valid = False
    while not valid:
         try:
             userInput = dataTypes[dataType](input(prompt))
             valid = True
         except ValueError:
             print("\nInvalid Input: Please enter a value of type " + dataType + "\n")
             continue
    return userInput

def save(profile, path):
    if not os.path.exists(path):
        print("File Directory not found. Attempting to create.")
        os.makedirs(path)
    with open(os.path.join(path, profile.name + '.sb'), 'wb') as sbfile:
        pickle.dump(profile, sbfile)

   
def mainMenu():
    mainMenu = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|           Main Menu            |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| 1. Create new profile          |
| 2. Export existing profiles    |
| 0. Exit                        |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    options = {'0' : lambda: None,
               '1' : createNewProfileMenu,
               '2' : exportProfilesMenu,
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
    while (option != '0'):
        option = mainMenu()

if __name__ == "__main__":
    main()
