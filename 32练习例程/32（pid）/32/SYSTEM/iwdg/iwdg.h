#ifndef _IWDG_
#define _IWDG_
#include "sys.h" 

void init_iwdg(u8 prer,u16 rlr);  //分频系数 计数值
void feed_iwdg();


#endif
