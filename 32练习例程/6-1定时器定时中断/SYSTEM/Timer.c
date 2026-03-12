#include "stm32f10x.h"                  // Device header

//1.打开时钟
//2.选择时基单元的时钟源
//3.配置时基单元(PSC预分频器，CNT计数器，ARR自动重装器)
//4.配置输出中断控制，允许更新中断输出到NVIC
//5.配置NVIC，在其打开定时器的中断通道，分配一个优先级
//6.使能定时器
//7.写定时器的中断函数


void Timer_Init(void)
{
	//初始通用定时器TIM2
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	
	//2
	TIM_InternalClockConfig(TIM2);
	
	//3
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;  //一分屏
	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; //向上计数
	           //定时一秒
	TIM_TimeBaseInitStructure.TIM_Period = 10000-1;    // 在10K的频率下计数10000   
	TIM_TimeBaseInitStructure.TIM_Prescaler =7200-1 ;  //对72MHZ进行7200分屏得到10K的计数频率
	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructure);
	
	//4
	TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE);           //因为向上计所以采用更新中断
	
	//5
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_Init(&NVIC_InitStructure);
	
	//6
	TIM_Cmd(TIM2,ENABLE);
	
}

   //7(这里放在主函数里了)

//void TIM2_IRQHandler(void)  //当定时器产生更新中断时，自动执行这个函数
//{
//	if(TIM_GetITStatus(TIM2,TIM_IT_Update) == SET)
//	{
//		Num ++;
//		TIM_ClearITPendingBit(TIM2,TIM_IT_Update);	//清除中断标志位
//	}
//	
//}






















