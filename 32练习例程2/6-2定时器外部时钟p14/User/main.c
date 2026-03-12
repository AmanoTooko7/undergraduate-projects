#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header
#include "LED.h"
#include "Key.h"
#include "OLED.h"
#include "Timer.h"
//------------------------相关函数作用---------------------//
//GPIO_SetBits(GPIOx, GPIO_Pin);把指定端口设置高电平
//GPIO_ResetBits(GPIOx, GPIO_Pin);设置低电平
//GPIO_WriteBit(GPIOx, GPIO_Pin, BitVal);
//GPIO_Write(GPIOx, PortVal);同时对16个端口写入

//GPIO_ReadInputDataBit(GPIOx, GPIO_Pin);读取输入寄存器某一个寄存器的值
//GPIO_ReadInputData(GPIOx);读取整个输入寄存器，返回一个16进制数据
//GPIO_ReadOutputDataBit(GPIOx, GPIO_Pin);读取输出寄存器某一个寄存器的值
//GPIO_ReadOutputData(GPIOx);读取整个输出寄存器，返回一个16进制数据

//OLED_ShowChar(Line, Column, char Char);在OLED屏幕上(line,column)显示一个字符
//OLED_ShowString(1, 3, "Hellow");显示字符串
//OLED_ShowNum(2, 1, 12345, 5);显示无符号数字12345，长度为5
//OLED_ShowSigneNum(2, 7 ,+77,2);显示有符号数字+77，长度为2
//OLED_ShowHexNum(3, 1,0xAA55, 4);显示十六进制数
//OLED_Sh显示二进制数owBinNum(4, 1,0xAA55, 16);显示二进制数
//OLED_Clear();清屏
//------------------------相关函数作用---------------------//


uint16_t Num;//全局变量

int main(void)
{
	
	OLED_Init();
	Timer_Init();
	OLED_ShowString(1, 1, "Num:");
	OLED_ShowString(2, 1, "Cou:");
	while(1)
	{
	  OLED_ShowNum(1, 5, Num, 5);
	  OLED_ShowNum(2, 5, TIM_GetCounter(TIM2), 5);//显示的是 TIM_TimeBaseInitStructure.TIM_Period = 10000 - 1的赋值9999

	}
}

//定时器TIM2产生更新中断时执行此函数
void TIM2_IRQHandler(void)
{
	if(TIM_GetITStatus(TIM2, TIM_IT_Update) == SET)
	{
		Num ++;

		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
	}
}

