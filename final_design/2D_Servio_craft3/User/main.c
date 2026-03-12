#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header
#include "LED.h"
#include "Key.h"
#include "OLED.h"
#include "Servo.h"
#include "Serial.h"
#include "timer.h"
#include "Move.h"
#include <math.h>
//下方舵机，左转增加

uint8_t KeyNum;//全局变量,按键

float up0 = 90;//初始化角度
float do0 = 90;

float up1 = 87.6 ;//---
float do1 = 95 ;  //---

float up2 = 87.5  ;
float do2 = 82.7  ;

float up3 =92.5      ;
float do3 = 83  ;

float up4 =90    ;
float do4 = 95.5    ;

int main(void)
{
	OLED_Init ();
	Servo_Init();
	Key_Init();
	Serial_Init();//串口初始化
	
	Servo_SetAngle_down(do0);
	Servo_SetAngle_up(up0);
	Delay_ms(2000);
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);//用的PB12为蜂鸣器的io口输出
	GPIO_InitTypeDef GPIO_InitStructure;  //这是结构体名字叫GPIO_InitTypeDef有GPIO_Mode,GPIO_Pin,GPIO_Speed三种类型
	//下三排作用为：GPIOA外设，0号引脚，配置为推挽输出(pp)，50MHz的速度
	//推挽输出高低电平都有驱动能力，
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure); 
	
	GPIO_SetBits(GPIOB, GPIO_Pin_12);
	Delay_ms(5000);
	/*以上为蜂鸣器配置*/
	
		int cnt = 4;
		while(cnt)//循环一次表示完成从一个点到另一个点的过程
			{
			
			float i1 = 0.07, i2 = 0.05, i3 = 0.1, i4 = 0.07, i5 = 0.07; //i1,i2分别用于下面和上面舵机的增量,下90-95(+5)，上90-87.6(-2.4)
																	    //i3,i4
			float contr_1;  //第一二两个contr用于从初始点到第一点
			float contr_2;
			float contr_3;  //第二三个用于，第一到2点，2到3点，3到4点
			float contr_4;
			float contr_5;
			while(1){    //循环结束表示到达第一点
					updatePoints();         //================
					do0 += i1;
					contr_1 = do0;
					if(contr_1 >= do1)  contr_1 = do1;
					Servo_SetAngle_down(contr_1);
					Delay_ms(70);
					
					up0 -= i2;
					contr_2 = up0;
					if(contr_2  <= up1)  contr_2 = up1;
					Delay_ms(70);
					Servo_SetAngle_up(contr_2);
					
				    if(contr_1 == do1 && contr_2 == up1)  {
						OLED_ShowString(1, 1,"ReachPoint");
						OLED_ShowNum(1, 11, 1, 1);
						TIM_Cmd(TIM2, DISABLE);
						break;//判断是否到达第一点
						}
				}
			
			GPIO_ResetBits(GPIOB, GPIO_Pin_12);//响500ms后关闭
			Delay_ms(800);
			GPIO_SetBits(GPIOB, GPIO_Pin_12);
			Delay_ms(500);
				
			
			TIM_Cmd(TIM2, ENABLE);
			cnt = 3;
						//需要从95到83，-12
			while(1){   //循环结束表示到达第二个点
					updatePoints();         //================
					do1 -= i3;
					contr_3 = do1;
					if(contr_3 <= do2) contr_3 = do2;
					Delay_ms(70);
					Servo_SetAngle_down(contr_3);
				
					if(contr_3 == do2) {
					OLED_ShowString(2, 1,"ReachPoint");
					OLED_ShowNum(2, 11, 2, 1);
					TIM_Cmd(TIM2, DISABLE);						
					break;
					}
			}
			
			GPIO_ResetBits(GPIOB, GPIO_Pin_12);//响800ms后关闭
			Delay_ms(800);
			GPIO_SetBits(GPIOB, GPIO_Pin_12);
			Delay_ms(500);
			
			Delay_ms(4000);
			TIM_Cmd(TIM2, ENABLE);
			cnt = 2;
			
			
			while(1){   //循环结束表示到达第三个点,上方舵机87.6到92.5，+4.9
				    updatePoints();         //================
					up2 += i4;
					contr_4 = up2;
					if(contr_4 >= up3) contr_4 = up3;
					Delay_ms(70);
					Servo_SetAngle_up(contr_4);
				
					if(contr_4 == up3) {
					OLED_ShowString(3, 1,"ReachPoint");
						OLED_ShowNum(3, 11, 3, 1);
					TIM_Cmd(TIM2, DISABLE);						
					break;
					}
			}
			
			GPIO_ResetBits(GPIOB, GPIO_Pin_12);//响500ms后关闭
			Delay_ms(800);
			GPIO_SetBits(GPIOB, GPIO_Pin_12);
			Delay_ms(500);
			
			Delay_ms(1000);
			TIM_Cmd(TIM2, ENABLE);
			cnt = 1;
			
			while(1){   //循环结束表示到达第三个点,上方舵机83到95.5，+12.5
					updatePoints();         //================
					do3 += i5;
					contr_5 = do3;
					if(contr_5 >= do4) contr_5 = do4;
					Delay_ms(70);
					Servo_SetAngle_down(contr_5);
				
					if(contr_5 == do4) {
					OLED_ShowString(4, 1,"ReachPoint");
					OLED_ShowNum(4, 11, 4, 1);
					TIM_Cmd(TIM2, DISABLE);						
					break;
					}
			}
			
			GPIO_ResetBits(GPIOB, GPIO_Pin_12);
			Delay_ms(800);
			GPIO_SetBits(GPIOB, GPIO_Pin_12);
			Delay_ms(500);
			
			Delay_ms(10000);
			cnt = 0;
			}


}









