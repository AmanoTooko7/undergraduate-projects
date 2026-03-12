#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header
#include "LED.h"
#include "Key.h"
#include "OLED.h"
#include "Serial.h"
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


uint8_t KeyNum;//全局变量

int main(void)
{
	OLED_Init();
	Serial_Init();
//	Serial_SendByte(0x41);//0x41对应字符A，括号里也可填"A",
//	uint8_t MyArray[] = {0x23, 0x33, 0x77, 0x32};
//	Serial_SendArray(MyArray, 4);//发送数组
	
//	Serial_SendString("hi! world\r\n");//发送字符

//  Serial_SendNumber(1234, 4);//发送数字

//	printf("Num=%d\r\n", 777);//最常用的方法，以下的两种可实现同样的效果
	
//	char String[100];
//	sprintf(String, "Num=%d\r\n", 777);
//	Serial_SendString(String);
	
//	Serial_Printf("\r\nNum=%d", 777);
//	Serial_Printf("\r\n");
	
	while(1)
	{
	  
	}

}
