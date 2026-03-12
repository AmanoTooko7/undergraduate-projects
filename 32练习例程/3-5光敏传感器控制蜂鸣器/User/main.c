#include "stm32f10x.h"
#include "Delay.h"
#include "Buzzer.h"
#include "LightSensor.h"


int main (void)
{
	
	Buzzer_Init();
	LightSensor_Init();
	
	while(1)
		
	{
		if(LightSensor_Get() == 0)  //为0表示光敏传感器受到光线比较暗的情况，向单片机传入电平0,也就是LED1的端口
		{
			Buzzer_ON();
		}
		else
		{
		  Buzzer_OFF();
		}
	}
		

}