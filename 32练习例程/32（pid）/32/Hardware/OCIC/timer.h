#ifndef __TIMER_H
#define __TIMER_H

#include "sys.h"


void TIM2_Int_Init(u16 arr,u16 psc);
void TIMx_calcPID_start(void);
void TIMx_calcPID_stop(void);


#endif
