#ifndef __PWM_H
#define __PWM_H

void PWM_Init(void);//初始化PWM使用哪个IO口输出
					//已经初始化PWM的输出频率，占空比


void PWM_SetCompare3(uint16_t Compare);//设置CCR的值，当AAR为100-1时，设置CCR的值就位占空比

#endif
