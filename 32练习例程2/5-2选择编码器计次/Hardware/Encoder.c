#include "stm32f10x.h"                  // Device header


void  Encoder_Init(void)
{
	//开启GPIOB和AFIO的时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);
	
	//配置GPIO
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;//上拉输入，高电平输入
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	//配置AFIO,因为这里我们用的是B0和B1口作为中断
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB , GPIO_PinSource0);
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB , GPIO_PinSource1);
	
	//初始化EXTI，
	EXTI_InitTypeDef EXTI_InitStructure;
	EXTI_InitStructure.EXTI_Line = EXTI_Line0 |  EXTI_Line1;
	EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;//中断响应而不是事件响应
	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;//规定是上升沿或下降沿，或上升下降沿触发
	EXTI_InitStructure.EXTI_LineCmd = ENABLE;
	EXTI_Init(&EXTI_InitStructure);
	
	//配置NVIC，用于对优先级分组还要初始化
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//两位抢占优先级两位响应优先级
	
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = EXTI0_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;//设置抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;//设置响应优先级
	  
	NVIC_InitStructure.NVIC_IRQChannel = EXTI1_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;//设置抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;//设置响应优先级
	
	NVIC_Init(&NVIC_InitStructure); 

}

int16_t Encoder_Count;
 
int16_t Encoder_Get(void)
{
	int16_t Temp;
	Temp = Encoder_Count;
	Encoder_Count = 0;
	return Temp;
}


//选择编码器正转B输出方波超前90度，反转滞后90
//见视频39分钟内容
//这里下面进入的是两个中断函数,右转进入第二个，左转进入第一个
void EXTI0_IRQHandler(void)
{
	if (EXTI_GetITStatus(EXTI_Line0) == SET)//判断是否是外部中断0号线触发的中断，检测中断标志位
	{
		if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0)
		{
			Encoder_Count--;
		}
		EXTI_ClearITPendingBit(EXTI_Line0);//清除中断标志位
	}
}

void EXTI1_IRQHandler(void)
{
	if (EXTI_GetITStatus(EXTI_Line1) == SET)
	{
		if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_0) == 0)
		{
			Encoder_Count++;
		}
		EXTI_ClearITPendingBit(EXTI_Line1);
	}
}
	









 