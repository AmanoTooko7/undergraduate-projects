#include "stm32f10x.h"                  // Device header


void LED_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2 | GPIO_Pin_3;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOC,&GPIO_InitStructure);
	
	GPIO_SetBits(GPIOC,GPIO_Pin_2 | GPIO_Pin_3);

}

void LED1_ON(void)
{
	GPIO_ResetBits(GPIOC,GPIO_Pin_2);
}

void LED1_OFF(void)
{
	GPIO_SetBits(GPIOC,GPIO_Pin_2);
}

void LED1_Turn(void)//这个函数用于实现PC2(LED1)的电平翻转
{
	if (GPIO_ReadOutputDataBit(GPIOC,GPIO_Pin_2) == 0)//如果读到LED1端口为0
	{
		GPIO_SetBits(GPIOC,GPIO_Pin_2);    							//将LED1置1
	}
	else
	{
		GPIO_ResetBits(GPIOC,GPIO_Pin_2);								//否则置0
	}
}

void LED2_ON(void)
{
	GPIO_ResetBits(GPIOC,GPIO_Pin_3);
}

void LED2_OFF(void)
{
	GPIO_SetBits(GPIOC,GPIO_Pin_3);
}

void LED2_Turn(void)//这个函数用于实现PC2(LED1)的电平翻转
{
	if (GPIO_ReadOutputDataBit(GPIOC,GPIO_Pin_3) == 0)
	{
		GPIO_SetBits(GPIOC,GPIO_Pin_3);
	}
	else
	{
		GPIO_ResetBits(GPIOC,GPIO_Pin_3);
	}
}
