#ifndef __SERVO_H
#define __SERVO_H

void Servo_Init(void);
void Servo_SetAngle_up(float Angle);//控制上方云台，PA1输出pwm
void Servo_SetAngle_down(float Angle);//控制下面云台，PA2

#endif
