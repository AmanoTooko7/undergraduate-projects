#include "stm32f10x.h"                  // Device header


//以下使用光敏传感器来进行计数工作，配置的端口GPIOC7
//注意所选的GPIO端口要与AFIO,EXIT,NVIC所选的通道要对应

uint32_t CountSensor_Count;

void CountSensor_Init(void)
{
	//时钟配置
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);
	
	//GPIO配置
	GPIO_InitTypeDef GPIO_InitStructure;         		
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;		//上拉输入，默认高电平输入
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_7 ;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOC,&GPIO_InitStructure);
	
	//下一句配置AFIO
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOC,GPIO_PinSource7);//代表连接PC7号口的第7个中断线路
	
	//配置EXIT
	EXTI_InitTypeDef EXTI_InitStructure;									 //以下几步配置EXIT
	EXTI_InitStructure.EXTI_Line = EXTI_Line7;            //将EXIT的线路7
	EXTI_InitStructure.EXTI_LineCmd = ENABLE;
	EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;    //配置为中断模式
	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;//下降沿触发
	EXTI_Init(&EXTI_InitStructure);
	
	//配置NVIC
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = EXTI9_5_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;//抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;			 //响应优先级
	NVIC_Init(&NVIC_InitStructure);
}

uint16_t CountSensor_Get(void)
{
	return CountSensor_Count;
}

void EXTI9_5_IRQHandler(void)     //中断函数
	{
		if(EXTI_GetITStatus(EXTI_Line7) == SET);
		{
			if (GPIO_ReadInputDataBit(GPIOC, GPIO_Pin_7) == 0)
			{
				Delay_s(1);
				if (GPIO_ReadInputDataBit(GPIOC, GPIO_Pin_7) == 0)
				{
			  CountSensor_Count++;
				}
			}
			EXTI_ClearITPendingBit(EXTI_Line7);//清除中断标志位
		}
	}
	
//	uint8_t LightSensor_Get(void)
//{
//	return GPIO_ReadInputDataBit(GPIOC, GPIO_Pin_2);
//}
	