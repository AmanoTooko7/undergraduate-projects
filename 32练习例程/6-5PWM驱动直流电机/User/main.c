#include "stm32f10x.h"
#include "Delay.h"
#include "OLED.h"
#include "Motor.h"



int main (void)
{
	OLED_Init();
	Motor_Init();
	Motor_SetSpeed(50);
	
	while(1)
	{

	}	
}