#include "stm32f10x.h"                  // Device header
#include <stdio.h>
#include <stdarg.h>

/*
1.开启USART和GPIO的时钟
2.GPIO初始化，把TX配置成复用输出。RX配置成输入
3.配置USART,使用结构体配置
4.只发送数据的功能就只需开启USART。若要接收数据那就在开启USART之前。再加ITConfig和NVIC的代码
*/

void Serial_Init(void){
	//1
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	//2
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;//将PA9配置为复用推挽输出GPIO_Mode_AF_PP
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	//3
	USART_InitTypeDef USART_InitStructure;
	USART_InitStructure.USART_BaudRate = 9600;//配置比特率
	USART_InitStructure.USART_WordLength = USART_WordLength_9b;//字长选择，因为不需要校验所以选择8位字长
	USART_InitStructure.USART_StopBits = USART_StopBits_1; //选择一位停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//选择无校验
	USART_InitStructure.USART_Mode = USART_Mode_Tx;//配置串口模式，将PA9配置为传输模式
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//硬件流控配置，这里不使用
	USART_Init(USART1, &USART_InitStructure);
	//4开启USART
	USART_Cmd(USART1 ,ENABLE);
}

//
void Serial_SendByte(uint8_t Byte){
	USART_SendData(USART1, Byte);//调用此函数传入的Byte就写入到TDR里了 
	while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);//这个USART_FLAG_TXE表示发送寄存器为空的标志位
	//RESET表示为0，当== RESET就一直进行while循环，当等于1(SET)时就脱离循环，表示得到了发送寄存器为空的标志位
																 //这个标志位会自动清零
}

void Serial_SendArray(uint8_t *Array, uint16_t Length){//用于发送数组Array,发送Length次
	uint16_t i;
	for (i = 0; i < Length; i++){
		Serial_SendByte(Array[i]);
	}
}

void Serial_SendString(char *String){//用于发送字符
	uint8_t i;
	for(i = 0; String[i] != '\0'; i++){
		Serial_SendByte(String[i]);
	}
}

uint32_t Serial_Pow(uint32_t X, uint32_t Y){//此函数输入XY后 输出为X^Y
	uint32_t Result = 1;
	while (Y --){
		Result *= X;
	}
	return Result;
}

void Serial_SendNumber(uint32_t Number, uint8_t Length){
	uint8_t i;
	for (i = 0; i < Length; i++){
		Serial_SendByte(Number / Serial_Pow(10, Length - i - 1) % 10 + '0');
	}
	  
}

int fputc(int ch, FILE *f){//此函数用于printf输出到串口
	Serial_SendByte(ch);
	return ch;
}

//封装Sprintf函数,C语言中可变参数用法，完全看不懂
void Serial_Printf(char *format, ...){
	char String[100];
	va_list arg;
	va_start(arg, format);
	vsprintf(String, format, arg);
	va_end(arg);
	Serial_SendString(String);
}



