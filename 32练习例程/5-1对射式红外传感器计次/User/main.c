#include "stm32f10x.h"
#include "Delay.h"
#include "OLED.h"
#include "CountSensor.h"

 //extern uint32_t CountSensor_Count;


int main (void)
{
	OLED_Init();
	CountSensor_Init();
//	LightSensor_Init();
	
	OLED_ShowString(1,1,"Count:");
	
	while(1)
		
	{
			OLED_ShowNum(1, 7, CountSensor_Get(), 5);

	}
		

}