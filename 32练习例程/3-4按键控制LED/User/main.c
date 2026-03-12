#include "stm32f10x.h"
#include "Delay.h"
#include "LED.h"
#include "Key.h"

uint8_t Key_Num;//是全局变量，与Key.c里的KeyNum是局部只适用于Key_GetNum()

int main (void)
{
	
	LED_Init();
	KEY_Init();
	
	
	while(1)
		
	{
		Key_Num = Key_GetNum();
		if(Key_Num == 1)//表示按键1按下
		{
			LED1_Turn();
		}
		if(Key_Num == 2)//表示按键2按下
		{
			LED1_Turn();
		}		
	}
		

}