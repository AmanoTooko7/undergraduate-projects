#ifndef _CONTROL_
#define _CONTROL_

#include "timer.h"
#include "capture.h"
#include "protocol.h"
#include "common.h"
#include "bsp_pid.h"
#include "motor.h"

void AutoReloadCallback();
int pwm_val_protect(int pwm_input);
void SetTargetMaxSpeed(int speed);
int GetTargetMaxSpeed(void);
static void speed_val_protect(float *speed_val);




#endif