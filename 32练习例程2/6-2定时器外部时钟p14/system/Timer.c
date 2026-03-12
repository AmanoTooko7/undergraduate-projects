#include "stm32f10x.h"                  // Device header

void Timer_Init(void)
{
	//开启定时器APB1中的TIM2
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
	//配置PA0
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;//采用上拉输入
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
//	//选择时基单元的时钟，这是内部时钟
//	TIM_InternalClockConfig(TIM2);
	
	//选择外部时钟,这里TIM_ExtTRGPolarity_Inverted表示上升沿触发
	TIM_ETRClockMode2Config(TIM2, TIM_ExtTRGPSC_OFF, TIM_ExtTRGPolarity_Inverted,  0x0F);//选择外部时钟模式2，时钟从TIM_ETR引脚输入
																						 //注意TIM2的ETR引脚固定为PA0，无法随意更改
																						 //最后一个滤波器参数加到最大0x0F，可滤除时钟信号抖动
	
	//配置时基单元预分频器，无CNT计数器的参数
	//CK_CNT_OV(定时频率,去倒数为定时时间)== CK_PSC / (PSC + 1)(ARR + 1)
	//这里的CK_PSC为72M，进行7200得到10k,再除以10000就是1秒  
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV4;//采样输入信号的采样频率，DIV1表示输入一分频
	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up;//向上计数模式
	TIM_TimeBaseInitStructure.TIM_Period = 10 - 1;//自动重装器值ARR的值,从1记到9
	TIM_TimeBaseInitStructure.TIM_Prescaler = 1 - 1;//预分频器值，也就是PSC,这里是用红外传感器模拟的外部时钟的频率，所以比较小
													//这里是外部时钟，如果天1-1表示遮挡1一次计数器+1，
													//若为2-1为遮挡2次计数器
	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;//重复计数器值，是高级定时器有的，这里不需要赋值0
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);
	
	//使能中断
	TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);
	
	//配置NVIC
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//两位抢占优先级两位响应优先级
	
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;//设置抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;//设置响应优先级
	NVIC_Init(&NVIC_InitStructure);
	
	//启动定时器
	TIM_Cmd(TIM2, ENABLE);
}

//定时器TIM2产生更新中断时执行此函数
/*
void TIM2_IRQHandler(void)
{
	if(TIM_GetITStatus(TIM2, TIM_IT_Update) == SET)
	{
		Num ++;

		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
	}
}
*/






