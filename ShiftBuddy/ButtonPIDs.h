/* These are preset definitions for taking
 * advantage of the TM1638 buttons available
 * for program. You can go ahead and switch these
 * to take advantage of whatever PID you would like,
 * simply look inside of the OBD.h file and choose a
 * definition or check Wikipedia and type in the hex
 * code for your desired PID.
*/

#ifndef BUTTONPIDS_H
#define BUTTONPIDS_H

#define BTN2_PID  PID_RPM
#define BTN3_PID  PID_SPEED
#define BTN4_PID  PID_ENGINE_LOAD
#define BTN5_PID  PID_THROTTLE
#define BTN6_PID  PID_ENGINE_OIL_TEMP
#define BTN7_PID  PID_INTAKE_TEMP
#define BTN8_PID  PID_BAROMETRIC

#endif
