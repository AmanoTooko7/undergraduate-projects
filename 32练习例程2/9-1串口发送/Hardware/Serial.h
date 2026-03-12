#ifndef _SERIAL__H
#define _SERIAL__H

#include <stdio.h>//主要用于printf这个函数


void Serial_SendByte(uint8_t Byte);//此函数用于从单片机PA9发送数据，无返回值
void Serial_Init(void);

void Serial_SendArray(uint8_t *Array, uint16_t Length);//用于发送自定义的数组Array,
													  //在主程序类似用法为uint8_t MyArray[] = {0x23, 0x33, 0x77, 0x32};
													  //Serial_SendArray(MyArray, 4);
													  
void Serial_SendString(char *String);//发送字符串用法例如Serial_SendString("hi! world");
									//若需要换行加上\r\n
									
uint32_t Serial_Pow(uint32_t X, uint32_t Y);//传入X,Y返回X^Y
void Serial_SendNumber(uint32_t Number, uint8_t Length);//第一个参数发送数字，第二个参数写数字长度
void Serial_Printf(char *format, ...);
#endif
