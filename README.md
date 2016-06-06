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
    
