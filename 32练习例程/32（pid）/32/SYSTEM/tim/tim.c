
#include "tim.h"

//定时器时间计算公式Tout = ((重装载值+1)*(预分频系数+1))/时钟频率;
//例如：1秒定时，重装载值=9999，预分频系数=7199 



void TIM3_Init(u16 arr,u16 psc){  //TIM3 初始化 arr重装载值 psc预分频系数
    TIM_TimeBaseInitTypeDef     TIM_TimeBaseInitStrue;
    
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE);//使能TIM3
    TIM3_NVIC_Init (); //开启TIM3中断向量
    //oc_th_gpioinit(); //初始化开启oc输出
    //oc_pwm_init(80);    //
    
	TIM_InternalClockConfig(TIM3);
    
    TIM_TimeBaseInitStrue.TIM_Period=arr; //设置自动重装载值
    TIM_TimeBaseInitStrue.TIM_Prescaler=psc; //预分频系数
    TIM_TimeBaseInitStrue.TIM_CounterMode=TIM_CounterMode_Up; //计数器向上溢出
    TIM_TimeBaseInitStrue.TIM_ClockDivision=TIM_CKD_DIV1; //时钟的分频因子，起到了一点点的延时作用，一般设为TIM_CKD_DIV1
    TIM_TimeBaseInit(TIM3,&TIM_TimeBaseInitStrue); //TIM3初始化设置
  //  TIM_ITConfig(TIM3, TIM_IT_Update, ENABLE);//使能TIM3中断    
    TIM_Cmd(TIM3,ENABLE); //使能TIM3
}
void oc_pwm_init(u16 ccr)
{
    TIM_OCInitTypeDef tim_oc_init;
    TIM_OCStructInit(&tim_oc_init);
    tim_oc_init.TIM_OCMode=TIM_OCMode_PWM1;
    tim_oc_init.TIM_OCPolarity=TIM_OCPolarity_Low;
    tim_oc_init.TIM_OutputState=TIM_OutputState_Enable;
    tim_oc_init.TIM_Pulse=ccr;
    
    TIM_OC2Init(TIM3,&tim_oc_init);
}
void oc_th_gpioinit()
{
    GPIO_InitTypeDef gpio_init_ch2;
    
    gpio_init_ch2.GPIO_Mode=GPIO_Mode_AF_PP;
    gpio_init_ch2.GPIO_Pin=GPIO_Pin_7;
    gpio_init_ch2.GPIO_Speed=GPIO_Speed_50MHz;
    GPIO_Init(GPIOA,&gpio_init_ch2);
}
void TIM3_NVIC_Init (void){ //开启TIM3中断向量
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;	
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x3;	//设置抢占和子优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0x3;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);
}
