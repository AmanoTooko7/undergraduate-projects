#ifndef _MOTOR_H
#define _MOTOR_H
#include "main.h"
#include "stm32f1xx_hal.h"
#include "pid.h"
#include "usart.h"
#include "control.h"


void set_motor_output(int pwm1,int pwm2,int pwm3,int pwm4);
void set_zhuanwan_output(int pwm);
void stop_motor(void);
void start_motor(void);
void ABS_motor(int pwm1,int pwm2);

#endif
