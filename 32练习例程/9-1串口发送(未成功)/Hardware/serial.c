#include "stm32f10x.h"  
#include "stdio.h"
#include "stdarg.h"

void Serial_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	USART_InitTypeDef USART_InitStructure;
	USART_InitStructure.USART_BaudRate = 9600;   //波特率设置
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None; //无硬件流控(?)
	USART_InitStructure.USART_Mode = USART_Mode_Tx;   //串口模式，这里为发送模式
	USART_InitStructure.USART_Parity = USART_Parity_No;  //无校验位
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//1为停止位
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;  //8位停止位
	USART_Init(USART1, &USART_InitStructure);
	
	USART_Cmd(USART1, ENABLE);
}

void Serial_SendByte(uint8_t Byte)  //发送一个十六进制的的数
{
	USART_SendData(USART1,Byte);//调用此函数可以将Byte写入到TDR？
	while(USART_GetFlagStatus(USART1,USART_FLAG_TXE) == RESET); //如果标志位TEX置1，就可以在TDR写入数据了
	
}

void Serial_SendArray(uint8_t *Array,uint16_t Length)   //发送的是数组
{
	uint16_t i;
	for(i=0;i<Length;i++)
	{
		Serial_SendByte(Array[i]);
	}
}

void Serial_SendString(char *String)   //这是发送的字符串
{
	uint8_t i;
	for(i=0;String[i]!=0;i++)
	{
		Serial_SendByte(String[i]);
	}
}

uint32_t Serial_Pow(uint32_t X,uint32_t Y)
{
	uint32_t Result = 1;
	while(Y--)
	{
		Result *= X;
	}
	return Result;
}


void Serial_SendNumber(uint32_t Number,uint8_t Length)//此函数用于发送数字
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		Serial_SendByte(Number/Serial_Pow(10,Length-i-1)%10+'0');
	}
}

int fputc(int ch,FILE *f)
{
	Serial_SendByte(ch);
	return ch;
}

void Serial_Printf(char *format,...)
{
	char String[100];
	va_list arg;
	va_start(arg,format);
	vsprintf(String,format,arg);
	va_end(arg);
	Serial_SendString(String);
}













