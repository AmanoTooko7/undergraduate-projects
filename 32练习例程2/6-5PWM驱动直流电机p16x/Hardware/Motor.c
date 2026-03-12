#include "stm32f10x.h"                  // Device header
#include "pwm.h"           

void Motor_Init(void){
	
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4 | GPIO_Pin_5;//初始化PA4和PA5，这两个脚用于控制电机的方向
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	PWM_Init();
}

void Motor_SetSpeed(uint8_t Speed){
	if (Speed >= 0){
		GPIO_SetBits(GPIOA, GPIO_Pin_4);//;把指定端口设置高电平
		GPIO_ResetBits(GPIOA, GPIO_Pin_5);//设置低电平
		PWM_SetCompare3(Speed);
	}
	
	else{
		GPIO_ResetBits(GPIOA, GPIO_Pin_4);//设置低电平
		GPIO_SetBits(GPIOA, GPIO_Pin_5);//;把指定端口设置高电平
		PWM_SetCompare3(-Speed);

	}
}
