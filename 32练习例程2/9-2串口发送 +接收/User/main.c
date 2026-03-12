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


uint8_t RxData;//全局变量

//此为串口接收程序，下面分别使用查询和中断两种方法
//查询流程：在主函数不断判断RXNE标志位，若置1就说明收到数据，调用ReceiveData,读取DR寄存器

int main(void)
{
	OLED_Init();
	OLED_ShowString(1, 1, "RxData:");
	Serial_Init();
	
	while(1){
//	  if (USART_GetFlagStatus(USART1, USART_FLAG_RXNE) == SET){//如果if成立，就说明收到程序
//		  RxData = USART_ReceiveData(USART1);//Returns the most recent received data by the USART1 peripheral.
//											 //这里不用清除标志位了
//		  OLED_ShowHexNum(1, 1,RxData, 7);
//		  }
		
		if (Serial_GetRxFlag() == 1){//如果if成立，就说明收到数据
			RxData = Serial_GetRxData();
			Serial_SendByte(RxData);
			OLED_ShowHexNum(1, 8,RxData, 2);
	}

}
}
