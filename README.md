      ____  _     _  __ _     ____            _     _           |
     / ___|| |__ (_)/ _| |_  | __ ) _   _  __| | __| |_   _     |
     \___ \| '_ \| | |_| __| |  _ \| | | |/ _` |/ _` | | | |    |
      ___) | | | | |  _| |_  | |_) | |_| | (_| | (_| | |_| |    |
     |____/|_| |_|_|_|  \__| |____/ \__,_|\__,_|\__,_|\__, |    |
                                                      |___/     |
                                                                |
    -------------------------------------------------------------
    -------------------------- Intro ----------------------------
    Shift Buddy is a Aruduino/Python package for creating a shift-light optimized for
    maximum performance. Shift Buddy offers a set of algorithms used for calculating the
    optimum shift point and configuring a profile specifically for each vehicle you own.
    
    The codebase is intentionally loosely coupled with hardware to allow people to branch
    out and use any which hardware one chooses. If you're not into making modifications,
    Shift Buddy is pre-configured to use affordable open sourced hardware and can be fully
    assembled for under $60. Enjoy.
    
    See demo videos located at the bottom of this page for more information.
    -------------------------------------------------------------
    ------------------------ Disclamer -------------------------- 
    I nor Shift Buddy am responsible for any damage to one's own or other's vehicle.
    I am also not responsible for any injuries or death which may occur when using
    this product and do not condone using this product on public roads.
    Keep your eyes on the road, user discression is advised.
    -------------------------------------------------------------
    -------------------------------------------------------------
    ---------------- Software Pre-requisites --------------------
    1. Python3.X - https://www.python.org/downloads/
    2. Numpy - http://www.scipy.org/install.html
    3. Matplotlib - http://matplotlib.org/users/installing.html
    4. Arduino IDE - https://www.arduino.cc/en/Main/Software
    4. ArduinoOBD - https://github.com/stanleyhuangyc/ArduinoOBD/tree/master/libraries/OBD
    5. TM1638 Library - https://github.com/rjbatista/tm1638-library
    -------------------------------------------------------------
    -------------------------------------------------------------
    ---------------- Hardware Pre-requisites --------------------
    1. Arduino (Type non-specific, Uno reccomended) - https://www.arduino.cc/en/Main/ArduinoBoardUno
    2. Freematics Arduino Adapter ( UART or l2C ) - http://freematics.com/products/
    3. TM1638 Display - http://www.dx.com/p/8x-digital-tube-8x-key-8x-double-color-led-module-81873
    -------------------------------------------------------------
    -------------------------------------------------------------
    ----------------- Installation Process ----------------------
    1. Install all pre-requisite Python software (ensure Numpy and Matplotlib are Python3.X compatable)
    2. Follow instructions for installing the ArduinoIDE and supporting ArduinoOBD and TM1638 Library
    3. Follow wiring matrix located in the docs folder
    -------------------------------------------------------------
    -------------------------------------------------------------
    ---------------- Configuration Process ----------------------
    1. Run the sbConfig tool from the command-line with the following command:
        Python3.X sbConfig.py
    2. Using the configuration tool, there are 3 main options to choose from:
        I. Create new profile
        II. Export existing profiles
        III. View existing profiles
    3. Follow directions below for detailed instructions on using these three functions
    -------------------------------------------------------------
    -------------------------------------------------------------
    ------------------ Create new profile -----------------------
    Create new profile can be done via two different paths, manually or via generating
    a torque curve. Manually implies when creating shift-points, you can pre-choose when
    the shift notification will occur per gear. Generating a torque curve has you enter in
    torque information from a Torque vs RPM graph and it will use interpolation to internally 
    build a torque curve and run the "Optimum Shift Points Algorithm" over the generated curve.
    
    1. Create manually
        I. Enter a name - This name shows up when switching profiles
        II. Enter the tire diameter in inches (Tire + wheel)
        III. Enter how many gears your transmission is
        IV. Enter the overalll gear ratio for each gear (Transmission gear ratio * final gear
            ratio, if your car doesn't have a final gear ratio, final gear ratio is 1.0)
        V. Enter a RPM of which you want to be notified to shift
        VI. Enter an early warning time (early warning buffer to account for shift time)
        VII. Enter a filepath for saving this profile (this creates .sb files used for export)
    
    2. Create with TQ curve
        I. Follow instructions I - IV above (1.)
        II. Choose an interpolation scheme (lagrange or linear), these schemes can be
            experimented with until you find your best result.
        III. Choose to plot your torque curve if you would like to see the linear vs
             lagrange graph. This can help with experimenting between the two and use
             to see if plot closely matches actual torque curve of the vehicle.
        IV. Enter the minimum RPM of your vehicle
        V. Enter the maximum RPM of your vehicle (REDLINE!)
        VI. Using a graph or any other method, enter torque values corrisponding
            with each requested RPM (min through max at 500 RPM increments)
        VII. Follow instructions VI - VII above (1.)
    -------------------------------------------------------------
    -------------------------------------------------------------
    --------------- Export existing profiles --------------------
    Export existing profiles exports .sb files in which you've created using the "Create
    new profile" function. Profile exportation works by generating a "ProfileManager.h"
    file which you will copy into the ShiftBuddy directory and upload to the Arduino.
    
    1. Enter the filepath containing all of your .sb Files
    2. Select all files which you would like to upload to the device, a list
       can be seen every time you select a profile for export.
    3. Enter 0 when finished (Finish export)
    4. Enter the filepath of the ShiftBuddy folder
    5. After successfully exported, open up the ShiftBuddy.ino file in the Arduino IDE
    6. Locate the Arduino device using the IDE (tools -> port)
    7. Press the upload button, once upload complete, the device has now been synced
       with the exported profiles (ignore warnings).
    -------------------------------------------------------------
    -------------------------------------------------------------
    ---------------- View existing profiles ---------------------
    View existing profiles allows you to look at various .sb files and view what was
    stored inside of them. This is useful for viewing other profiles you may have forgotten
    about or sharing with other people.
    
    1. Profile path
        I. Enter the path directly to the .sb file to see information about that specific file
    2. Profile directory
        I. Enter the folder path to see a list of files and view each one individually
    -------------------------------------------------------------
    -------------------------------------------------------------
    -------------------------- Demos ----------------------------
    This was made for my senior capstone project, I've made some demo videos if you'd like
    to see the progress of its design and then a demo/presentation of the actual project.
    1. Very early stages - https://www.youtube.com/watch?v=1jm2bXmtqY0
    2. Stupid commercial (funny) - https://vimeo.com/166303353
    3. Final demo/presentation - TBD
    -------------------------------------------------------------
    -------------------------------------------------------------
    ----------------------- Final words -------------------------
    This project was designed to use a small set of cheap hardware, I intentionally
    designed the code to be loosely coupled with the hardware so anyone with minimal
    programming expertise could implement the Shift Buddy using their own hardware.
    (Arduino neccecary). 
    
    Here are a list of functions and code which can be changed if you'd like to swap
    outthe hardware:
    1. Read neccecary data:
      // obd.read(PID_SPEED, currentSpeedKPH); - Pull the speed in KPH
      // obd.read(PID_RPM, currentRPM); - Pull the RPM
      // obd.read(currentPID, currentPIDData); - This is only for vanity, ignore if your display
      //                                         doesn't output information
    2. Setup() - Modify the setup to use any new display or OBDII reader
    3. Modify ButtonLogic() - For implenting your own button for switching profiles if you'd like
    4. SignalUpshift() - This function Contains all logic for how you want the driver to see
                         the up-shift notification
    5. updateLEDs() - Modify display logic for adapting to how your device's LEDs signal green,
                      orange, and red.
    6. Aaaaaaand thats it! Enjoy. :)
    -------------------------------------------------------------
    -------------------------------------------------------------
