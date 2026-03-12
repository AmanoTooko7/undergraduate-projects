
#include "NVIC.h"

u8 INT_MARK;//中断标志位

void KEYPAD4x4_INT_INIT (void){	 //按键中断初始化
	NVIC_InitTypeDef  NVIC_InitStruct;	//定义结构体变量
	EXTI_InitTypeDef  EXTI_InitStruct;
    GPIO_InitTypeDef gpio_key;
    
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE); //启动GPIO时钟 （需要与复用时钟一同启动）     
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);//配置端口中断需要启用复用时钟

    gpio_key.GPIO_Mode=GPIO_Mode_IPU;
    gpio_key.GPIO_Pin=GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15;
    GPIO_Init(GPIOB,&gpio_key);
//第1个中断	
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource13);  //定义 GPIO  中断
	
	EXTI_InitStruct.EXTI_Line=EXTI_Line13;  //定义中断线
	EXTI_InitStruct.EXTI_LineCmd=ENABLE;              //中断使能
	EXTI_InitStruct.EXTI_Mode=EXTI_Mode_Interrupt;     //中断模式为 中断
	EXTI_InitStruct.EXTI_Trigger=EXTI_Trigger_Falling;   //下降沿触发
	
	EXTI_Init(& EXTI_InitStruct);
	
	NVIC_InitStruct.NVIC_IRQChannel=EXTI15_10_IRQn;   //中断线     
	NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;  //使能中断
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=2;  //抢占优先级 2
	NVIC_InitStruct.NVIC_IRQChannelSubPriority=2;     //子优先级  2
	NVIC_Init(& NVIC_InitStruct);
	
//第2个中断	
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource14);  //定义  GPIO 中断
	
	EXTI_InitStruct.EXTI_Line=EXTI_Line14;  //定义中断线
	EXTI_InitStruct.EXTI_LineCmd=ENABLE;              //中断使能
	EXTI_InitStruct.EXTI_Mode=EXTI_Mode_Interrupt;     //中断模式为 中断
	EXTI_InitStruct.EXTI_Trigger=EXTI_Trigger_Falling;   //下降沿触发
	
	EXTI_Init(& EXTI_InitStruct);
	
	NVIC_InitStruct.NVIC_IRQChannel=EXTI15_10_IRQn;   //中断线
	NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;  //使能中断
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=2;  //抢占优先级 2
	NVIC_InitStruct.NVIC_IRQChannelSubPriority=2;     //子优先级  2
	NVIC_Init(& NVIC_InitStruct);

//第3个中断	
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource15);  //定义  GPIO 中断
	
	EXTI_InitStruct.EXTI_Line=EXTI_Line15;  //定义中断线
	EXTI_InitStruct.EXTI_LineCmd=ENABLE;              //中断使能
	EXTI_InitStruct.EXTI_Mode=EXTI_Mode_Interrupt;     //中断模式为 中断
	EXTI_InitStruct.EXTI_Trigger=EXTI_Trigger_Falling;   //下降沿触发
	
	EXTI_Init(& EXTI_InitStruct);
	
	NVIC_InitStruct.NVIC_IRQChannel=EXTI15_10_IRQn;   //中断线
	NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;  //使能中断
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=2;  //抢占优先级 2
	NVIC_InitStruct.NVIC_IRQChannelSubPriority=2;     //子优先级  2
	NVIC_Init(& NVIC_InitStruct);

//第4个中断	
//    GPIO_EXTILineConfig(GPIO_PortSourceGPIOA, GPIO_PinSource7);  //定义  GPIO 中断

//    EXTI_InitStruct.EXTI_Line=EXTI_Line7;  //定义中断线
//    EXTI_InitStruct.EXTI_LineCmd=ENABLE;              //中断使能
//    EXTI_InitStruct.EXTI_Mode=EXTI_Mode_Interrupt;     //中断模式为 中断
//    EXTI_InitStruct.EXTI_Trigger=EXTI_Trigger_Falling;   //下降沿触发

//    EXTI_Init(& EXTI_InitStruct);

//    NVIC_InitStruct.NVIC_IRQChannel=EXTI9_5_IRQn;   //中断线
//    NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;  //使能中断
//    NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=2;  //抢占优先级 2
//    NVIC_InitStruct.NVIC_IRQChannelSubPriority=2;     //子优先级  2
//    NVIC_Init(& NVIC_InitStruct);

}

void  EXTI4_IRQHandler(void){

}
void  EXTI15_10_IRQHandler(void){
    
    if(EXTI_GetITStatus(EXTI_Line13)!=RESET){//判断某个线上的中断是否发生 
            if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_13)==Bit_RESET)
            {
                while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_13)==Bit_RESET);
                INT_MARK=1;
                
            }     
            EXTI_ClearITPendingBit(EXTI_Line13);   //清除 LINE 上的中断标志位

    }     
	else if(EXTI_GetITStatus(EXTI_Line14)!=RESET){//判断某个线上的中断是否发生 

            if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_14)==Bit_RESET)
            {
                while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_14)==Bit_RESET);
                INT_MARK=2;
                //GPIO_WriteBit(LEDPORT,LED1,(BitAction)(1-GPIO_ReadOutputDataBit(LEDPORT,LED1))); //取反LED1
                
                
            }
            EXTI_ClearITPendingBit(EXTI_Line14);   //清除 LINE 上的中断标志位
	}     
	else if(EXTI_GetITStatus(EXTI_Line15)!=RESET){//判断某个线上的中断是否发生 
            if(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_15)==Bit_RESET)
            {
                while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_15)==Bit_RESET);
                INT_MARK=3;
                //GPIO_WriteBit(LEDPORT,LED1,(BitAction)(1-GPIO_ReadOutputDataBit(LEDPORT,LED1))); //取反LED1           
            }
            EXTI_ClearITPendingBit(EXTI_Line15);   //清除 LINE 上的中断标志位
	}     
//	if(EXTI_GetITStatus(EXTI_Line7)!=RESET){//判断某个线上的中断是否发生 
//		INT_MARK=4;//标志位置1，表示有按键中断
//		EXTI_ClearITPendingBit(EXTI_Line7);   //清除 LINE 上的中断标志位
//	}     
}





