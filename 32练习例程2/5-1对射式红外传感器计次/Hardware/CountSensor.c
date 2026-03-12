#include "stm32f10x.h"                  // Device header

//GPIO_EXTILineConfig(GPIO_PortSourceGPIOB , GPIO_PinSource14);
//此函数，用于配置AFIO数据选择器，选择想要的中断引脚
//EXTI_GenerateSWInterrupt(EXTI_Line);软件触发一次中断线;
//EXTI_GetITStatus();用于判断中断标志位


uint16_t CountSensor_Count;

void CountSensor_Init(void)
{
	//开启GPIOB和AFIO的时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);
	
	//配置GPIO，选择P14
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;//上拉输入，高电平输入
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_14;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	//配置AFIO
	 GPIO_EXTILineConfig(GPIO_PortSourceGPIOB , GPIO_PinSource14);
	
	//初始化EXTI，
	EXTI_InitTypeDef EXTI_InitStructure;
	EXTI_InitStructure.EXTI_Line = EXTI_Line14;//因为端口是PB14所以选择线路14
	EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;//中断响应而不是事件响应
	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;//规定是上升沿，下降沿，或上升下降沿触发
	EXTI_InitStructure.EXTI_LineCmd = ENABLE;
	EXTI_Init(&EXTI_InitStructure);
	
	//配置NVIC，用于对优先级分组还要初始化
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//两位抢占优先级两位响应优先级
	
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = EXTI15_10_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;//设置抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;//设置响应优先级
	
	NVIC_Init(&NVIC_InitStructure);

}

uint16_t CountSensor_Get(void)
{
	return CountSensor_Count;
}



//中断函数执行程序,此函数名在启动函数上看！这里我们用的是 EXTI_Line14
void EXTI15_10_IRQHandler(void)
{
	//先进行中断标志位，用于判断如果是为EXTI14
	if (EXTI_GetITStatus(EXTI_Line14) == SET);
	{
		 CountSensor_Count ++;
		
		EXTI_ClearITPendingBit(EXTI_Line14);//要清除EXTI14的中断标志位，否则会一直请求中断
	}
}











