#include "led.h"
#include "stm32f10x.h"
void LED_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC ,ENABLE);//使能GPIOB的时钟
//	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD ,ENABLE);//使能GPIOE的时钟
	
	GPIO_InitStructure.GPIO_Mode= GPIO_Mode_Out_PP;   //以下两段分别对LED0,1设置
	GPIO_InitStructure.GPIO_Pin= GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Speed= GPIO_Speed_50MHz;
	GPIO_Init(GPIOC,&GPIO_InitStructure);
	GPIO_SetBits(GPIOC,GPIO_Pin_2);
	
	GPIO_InitStructure.GPIO_Mode= GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin= GPIO_Pin_3;
	GPIO_InitStructure.GPIO_Speed= GPIO_Speed_50MHz;
	GPIO_Init(GPIOC,&GPIO_InitStructure);
	GPIO_SetBits(GPIOC,GPIO_Pin_3);

}
