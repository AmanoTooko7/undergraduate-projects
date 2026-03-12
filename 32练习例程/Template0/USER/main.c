#include "stm32f10x.h"
#include"led.h"
#include"delay.h"

int main(void)
{
delay_init();  //对延时函数和LED都要初始化
LED_Init();
	
	while(1){
		
 			GPIO_SetBits(GPIOC,GPIO_Pin_2|GPIO_Pin_3);     //设置A,D为高电平(不亮)
//		GPIO_SetBits(GPIOC,GPIO_Pin_3);
			delay_ms(500);
		
			GPIO_ResetBits(GPIOC,GPIO_Pin_2|GPIO_Pin_3);		//设置A,D为低电平(亮) 
//		GPIO_ResetBits(GPIOC,GPIO_Pin_3);
		  delay_ms(500);
		
	}

}

