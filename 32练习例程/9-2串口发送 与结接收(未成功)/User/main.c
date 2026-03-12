#include "stm32f10x.h"
#include "Delay.h"
#include "OLED.h"

uint8_t RxData;

int main (void)
{
	OLED_Init();
	OLED_ShowString(1,1,"RxData:");
	
  Serial_Init();
	
	
	while(1)
		
	{
		if (Serial_GetRxFlag()==1)
		{
			RxData=Serial_GetRxData();
			Serial_SendByte(RxData);
			OLED_ShowHexNum(1,1,RxData,2);
		}

	}
		

}