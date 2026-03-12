#include "stm32f10x.h"                  // Device header
#include "pwm.h"   

void Servo_Init(void) {
	PWM_Init();
}

void Servo_SetAngle_up(float Angle){//控制上方云台，PA1输出pwm
	PWM_SetCompare2(Angle/110*2000 + 500);
}

void Servo_SetAngle_down(float Angle){//控制下面云台，PA2
	PWM_SetCompare3(Angle/170*2000 + 500);
}

