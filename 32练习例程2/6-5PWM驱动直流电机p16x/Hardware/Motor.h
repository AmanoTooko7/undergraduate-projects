#ifndef __MOTOR_H
#define __MOTOR_H

void Motor_SetSpeed(uint8_t Speed);//传入的Speed参数就相当于占空比，占空比越大转的越快
void Motor_Init(void);//初始化PA4和PA5，这两个脚用于控制电机的方向


#endif
