#include "stm32f10x.h"                  // Device header
#include "Delay.h"

void KEY_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Pin =	GPIO_Pin_13;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	GPIO_Init(GPIOC,&GPIO_InitStructure);
}

uint8_t Key_GetNum(void)//读取按键值的函数，调用可返回按键的键码,uint_t就是unsigned char的意思
{
	uint8_t KeyNum = 0;   //定义一个变量(这个变量不表示电平)用于表示是哪个按键按下，0没有按键按下
	if (GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_0) == 1)//读入Key1电平,(电平等于0表示按下)如果按下
		{
			Delay_ms(20);  //以下三排用于消抖
			while(GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_0) == 1);
			Delay_ms(20);
			KeyNum = 1;//表示按键1按下
		}
		
	if (GPIO_ReadInputDataBit(GPIOC,GPIO_Pin_13) == 1)//读入Key2电平,(电平等于0表示按下)如果按下
		{
			Delay_ms(20);  //以下三排用于消抖
			while(GPIO_ReadInputDataBit(GPIOC,GPIO_Pin_13) == 1);
			Delay_ms(20);
			KeyNum = 2;//按键2按下
		}		
		
	
	return KeyNum;
}