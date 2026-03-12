#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header
#include "LED.h"
#include "Key.h"
#include "OLED.h"
#include "Servo.h"
#include "Serial.h"
#include "timer.h"
//来源于6-4PWM驱动直流电机
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
//OLED_ShowBinNum(4, 1,0xAA55, 16);显示二进制数
//OLED_Clear();清屏
//------------------------相关函数作用---------------------//


uint8_t KeyNum;//全局变量,按键
//up角度减小，激光点向上，down角度减小激光点向右

float Init_Angle_up = 90;//初始化角度
float Init_Angle_down = 90;

float Angle_up1 = 85      ;    
float Angle_down1 = 95    ;

float Angle_up2 =98       ;    
float Angle_down2 = 89.5  ;

float Angle_up3 =105      ;    
float Angle_down3 = 89.5  ;

float Angle_up4 =105.5    ;    
float Angle_down4 = 103   ;



int main(void)
{ 
	
	OLED_Init ();
	Servo_Init();
	Key_Init();
	Serial_Init();//串口初始化
	OLED_ShowString(1, 1, "Laser:");
	OLED_ShowString(2, 1, "Recta:");
	
//	Servo_SetAngle_up(Init_Angle_up);
//	Delay_ms(500);
//	Servo_SetAngle_down(Init_Angle_down);
//	Delay_ms(500);

	while(1)
	{
		if (Serial_GetRxFlag() == 1) // 如果接收到数据包
        {
			OLED_Clear();
			OLED_ShowNum(1, 7, a, 3);
			OLED_ShowNum(1, 10, b,3);
            OLED_ShowNum(3, 7, x1, 3);
            OLED_ShowNum(3, 10, y1, 3);

        }
	}

}
