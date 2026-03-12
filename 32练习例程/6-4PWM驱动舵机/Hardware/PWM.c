#include "stm32f10x.h"                  // Device header


//1.开启TIM和GPIO的时钟
//2.配置时基单元
//3.配置输出比较单元(CCR的值，输出比较模式，极性选择)
//4.配置PWM对应的GPIO口
//5.启动计数器

void PWM_Init(void)
{
  //初始通用定时器TIM2
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	
	//在tim2的oc1通道上可以输出pwm波形,根据引脚定义只能在PA0输出pwm波形
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	
	TIM_InternalClockConfig(TIM2);
	
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;  //一分屏
	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; //向上计数
	           //定时一秒
	TIM_TimeBaseInitStructure.TIM_Period = 20000-1;    // ARR
	TIM_TimeBaseInitStructure.TIM_Prescaler =72-1 ;  //PSC
	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;             //这里通过ARR,PSC,CCR设置一个频率为1KHz
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructure);               //占空比0.5，分辨率1%的PWM波形
	
	TIM_OCInitTypeDef TIM_OCInitStructure;
	TIM_OCStructInit(&TIM_OCInitStructure);
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;								//设置输出比较的模式
  TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;				//设置输出比较的极性
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;		//设置输出使能
	TIM_OCInitStructure.TIM_Pulse = 0;																//设置CCR的值
	TIM_OC2Init(TIM2,&TIM_OCInitStructure);  //表示在tim2的oc1通道上可以输出pwm波形了
	
	TIM_Cmd(TIM2,ENABLE);
	 
}

void PWM_SetCompare2(uint16_t Compare) 
{
	TIM_SetCompare2(TIM2,Compare);  //这个函数是直接设置CCR的值
}



