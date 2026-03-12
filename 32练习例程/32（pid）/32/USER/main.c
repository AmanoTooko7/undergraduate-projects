#include "stm32f10x.h" //STM 头文件
#include "sys.h"
#include "delay.h"
#include "stdio.h"
#include "NVIC.h"
#include "usart.h"
#include "timer.h"
#include "capture.h"
#include "pwm.h"
#include "protocol.h"
#include "control.h"


void led_init()
{
    GPIO_InitTypeDef LED_GPIOC;
    
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);
    LED_GPIOC.GPIO_Mode=GPIO_Mode_Out_PP;
    LED_GPIOC.GPIO_Pin=GPIO_Pin_13;
    LED_GPIOC.GPIO_Speed=GPIO_Speed_50MHz;
    GPIO_Init(GPIOC,&LED_GPIOC);
    
}
int main (void)
{ 	
    
    int32_t target_speed;
    
    RCC_Configuration(); //时钟设置
    NVIC_Configuration();
    //SysTick_Config(9000000);  //1s
    //SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK_Div8);
    //NVIC_SetPriority(SysTick_IRQn,1);
    uart_init(115200);
    delay_ms(500);
    //usart1_send("222",4);
    TIMx_pwm_init(1000,72); //不分频。PWM 频率=72000/(899+1)=80Khz
    TIM2_Int_Init(99,7199);
    TIMx_encoder_init();
    protocol_init();
    PID_param_init();
    TIM_SetCompare2(TIM3,0);
    TIM_SetCompare1(TIM3,0);
    led_init();
    PCout(13)=1;
    
    //TIM_SetCompare3(TIM3,500);
#if defined(PID_ASSISTANT_EN)
	/*初始化时，上发stop，同步上位机的启动按钮状态*/
	set_computer_value(SEND_STOP_CMD, CURVES_CH1, NULL, 0);  

	/*获取默认的目标值*/
	target_speed = (int32_t)get_pid_target(&pid_speed);
	/*给通道1发送目标值*/
	set_computer_value(SEND_TARGET_CMD, CURVES_CH1, &target_speed, 1);     
#endif
 while(1)
 {      

    //TIM_SetCompare2(TIM3,500);  //20~100
   receiving_process();
   
     
 } 
}

void SysTick_Handler(void)
{
    PCout(13)=~PCout(13);              
}

