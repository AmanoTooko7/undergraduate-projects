#ifndef  __PWM_H
#define  __PWM_H
#include "sys.h"

void TIM3_Init(u16 arr,u16 psc);
void TIM3_NVIC_Init (void);
void oc_th_gpioinit();
void oc_pwm_init(u16 ccr);


#endif
