#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header
#include "LED.h"
#include "Key.h"
#include "Buzzor.h"
#include "LightSensor.h"

//------------------------相关函数作用---------------------//
//GPIO_SetBits(GPIOx, GPIO_Pin);把指定端口设置高电平
//GPIO_ResetBits(GPIOx, GPIO_Pin);设置低电平
//GPIO_WriteBit(GPIOx, GPIO_Pin, BitVal);
//GPIO_Write(GPIOx, PortVal);同时对16个端口写入

//GPIO_ReadInputDataBit(GPIOx, GPIO_Pin);读取输入寄存器某一个寄存器的值
//GPIO_ReadInputData(GPIOx);读取整个输入寄存器，返回一个16进制数据
//GPIO_ReadOutputDataBit(GPIOx, GPIO_Pin);读取输出寄存器某一个寄存器的值
//GPIO_ReadOutputData(GPIOx);读取整个输出寄存器，返回一个16进制数据

//------------------------相关函数作用---------------------//


uint8_t KeyNum;//全局变量

int main(void)
{
	Key_Init();
	BUZZOR_Init();
	LightSensor_Init();

	while(1)
	{
		
		if (LightSensor_Get() == 1)		//如果当前光敏输出1
		{
			Buzzor_ON();				//蜂鸣器开启
		}
		else							//否则
		{
			Buzzor_OFF();				//蜂鸣器关闭
		}
		
		
//		if (Key_GetNum()  == 1)//此程序用按键PB1控制蜂鸣器是否发声
//		{
//			Buzzor_ON();
//			//a = a + 1;
//		}
//		if (Key_GetNum()  == 1)
//		{
//			//a = a - 1;
//			Buzzor_OFF();
//		}
	}

}
