#include "stm32f10x.h"                  // Device header

//TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;   //设置输出比较的模式，一般用pwm模式1，向上计数cnt<ccr置有效电平
//TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;//设置输出比较的极性
															//TIM_OCPolarity_High 高电平为有效
															//TIM_OCPolarity_Low 低电平为有效

//TIM_SetCompare1(TIM_TypeDef* TIMx, uint16_t Compare1);改写通道1CCR的值

void PWM_Init(void)
{
		//开启定时器APB1中的TIM2
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
	
	//以下这段由于我使用的是TIM2_CH1根据引脚定义默认复用功能是映射到PA0上，所以要使用GPIO初始化
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	

/*加上以下三排将PA0重映射到PA15,注意更改GPIO口的初始化
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);//对重映射的时钟初始化
	GPIO_PinRemapConfig(GPIO_PartialRemap1_TIM2, ENABLE);//对TIM2重映射，第一个参数选择部分重映射1
														//把PA0换到PA15
														//见参考手册119表43
	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable, ENABLE);//解除原本PA15，PB3,4原本的JTAG的作用重映射才能起作用
	//这三句的作用就是PA15做PA0的功能了，而不用PA0了，所以下面就需要初始化PA15了

*/	
	
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;//这里是使用定时器来控制的引脚所以必须用GPIO_Mode_AF_PP
													//而GPIO_Mode_Out_PP是常用的
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	
	//选择时基单元的时钟
	TIM_InternalClockConfig(TIM2);
	
	//配置时基单元预分频器，无CNT计数器的参数
	//CK_CNT_OV(定时频率,去倒数为定时时间)== CK_PSC / (PSC + 1)(ARR + 1)
	//这里的CK_PSC为72M，进行7200得到10k,再除以10000就是1秒  
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;//采样输入信号的采样频率，DIV1表示输入一分频
	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up;//向上计数模式
	TIM_TimeBaseInitStructure.TIM_Period = 100 - 1;//自动重装器值ARR的值，也就是计数器
	TIM_TimeBaseInitStructure.TIM_Prescaler = 720 - 1;//预分频器值，也就是PSC
	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;//重复计数器值，是高级定时器有的，这里不需要赋值0
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);
	
	//初始化输出比较通道,不同的通道对应的GPIO口不一样，这里使用的是PA0，对应第一个输出比较通道
	TIM_OCInitTypeDef TIM_OCInitStructure;
	TIM_OCStructInit(&TIM_OCInitStructure);					//还有其他结构体成员未列出，此函数用于给以下四个参数赋初值
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;   	//设置输出比较的模式，一般用pwm模式1，向上计数cnt<ccr置有效电平
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;//设置输出比较的极性
															//TIM_OCPolarity_High 高电平为有效
															//TIM_OCPolarity_Low 低电平为有效
		
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;//设置输出使能
	TIM_OCInitStructure.TIM_Pulse = 0;						//设置CCR的，调节多少占空比就是多少
	TIM_OC1Init(TIM2, &TIM_OCInitStructure);//v这里使用的是PA0，对应第一个输出比较通道，在TIM2上OC1通道，见引脚定义默认复用功能
	
	//启动定时器
	TIM_Cmd(TIM2, ENABLE);
	
	/*
	这三句是用来确定PWM的频率F，占空比D，分辨率的R的
	见ppt69页，主频为也就是CK_PSC为72m，这里设置的频率为1000，占空比为50%，分辨率为1%
	TIM_TimeBaseInitStructure.TIM_Period = 100 - 1;//自动重装器值ARR的值，也就是计数器
	TIM_TimeBaseInitStructure.TIM_Prescaler = 720 - 1;//预分频器值，也就是PSC
	TIM_OCInitStructure.TIM_Pulse = 50;						//设置CCR的
	*/
	
}

//此函数用于更改通道1的CCR值，见PPT51页，
void PWM_SetCompare1(uint16_t Compare)
{
	TIM_SetCompare1(TIM2, Compare);
}
