#include "stm32f10x.h"
#include "Delay.h"
#include "OLED.h"
#include "Timer.h"

uint16_t num;


int main(void)
{
	OLED_Init();
	Timer_Init();

	OLED_ShowString(1, 1, "Num:");
	OLED_ShowString(2, 1, "CNT:");	
	while (1)
	{
		OLED_ShowNum(1, 5, num, 5);
		OLED_ShowNum(2, 5, Timer_GetCounter(), 5);
		
	}
}



void TIM2_IRQHandler(void)  //当定时器产生更新中断时，自动执行这个函数
{
	if(TIM_GetITStatus(TIM2,TIM_IT_Update) == SET)
	{
		num ++;
		TIM_ClearITPendingBit(TIM2,TIM_IT_Update);	//清除中断标志位
	}
	
}

