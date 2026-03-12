#include "led.h"
#include "stm32f10x.h"

void LED_Init(void){

	 //以下两排分别是对mini板两个LED端使能时钟
	 //RCC->APB2ENR|=1<<2;
	 //RCC->APB2ENR|=1<<5;
	 
	 //野火板两个LED的端口C使能时钟
	  RCC->APB2ENR|=1<<4;
	
		//以下两句相当于对GPIO的初始化
		GPIOC->CRL&=0xFF0FFFFF;
		GPIOC->CRL|=0x00300000;
	
		GPIOC->ODR|=1<<4;
}