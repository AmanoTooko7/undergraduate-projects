#include "led.h"
#include "delay.h"
#include "ultrasonsic.h"
#include "sys.h"
#include "lcd.h"
#include "usart.h"
#include "beep.h"

 int main(void)
 {	 
			    
	float length;    	   

	delay_init();	    	
	uart_init(115200); //初始化串口，波特率115200 	
//	LED_Init();	//初始化LED		
//	BEEP_Init();//初始化蜂鸣器 
	initHcsr04();	  							   
//	LED0 = 1;//上电默认绿灯亮
		
	while(1){
			
		length=Hcsr04GetLength();	//获取距离
		printf("dis = %fcm\r\n",length);//串口打印距离
		delay_ms(50);
//		if(length < 10){//小于10cm亮红灯绿灯灭
//			LED0 = 0;
//			LED1 = 1;
//			BEEP = 1;	
//			delay_ms(300);
//				
//		}else{
//			LED0 = 1;
//			LED1 = 0;
//			BEEP = 0;
//		}
//			
	}



	} 
