#ifndef _CONTROL_H
#define _CONTROL_H
#include "main.h"
#include "stm32f1xx_hal.h"
#include "pid.h"
#include "usart.h"
#include "motor.h"
#include "oled.h"
#include "nrf24l01.h"

extern float servo_sum;
extern float set_pwm;
extern char start_flag,stop_flag;
extern char exit_scanl,exit_scanr;
extern char process_flag;
extern char stop_5s_flag;
extern char stop_5s_flag_u;
extern char key_count;

extern uint8_t tim4_flag;
void PROCESS_MOTOR(void);
char click_M(void);
char click_STAR(void);
void key_proce(void);
void oled_display_speedlevel(void);
void mode_trans(void);

#endif
