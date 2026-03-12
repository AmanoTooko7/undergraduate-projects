#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header


//-----------相关函数作用---------------------//
//GPIO_SetBits(GPIOx, GPIO_Pin);把指定端口设置高电平
//GPIO_ResetBits(GPIOx, GPIO_Pin);设置低电平
//GPIO_WriteBit(GPIOx, GPIO_Pin, BitVal);
//GPIO_Write(GPIOx, PortVal);同时对16个端口写入

//-----------相关函数作用---------------------//



int main(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);//都是GPIOA的端口
	
    GPIO_InitTypeDef GPIO_InitStructure;  //这是结构体
	//下三排作用为：GPIOA外设，0号引脚，配置为推挽输出(pp)，50MHz的速度
	//推挽输出高低电平都有驱动能力，
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_All;//把GPIO0-15共16个端口全部配置了
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure); 
	
	//GPIO_SetBits(GPIOA, GPIO_Pin_0);
	//GPIO_ResetBits(GPIOA, GPIO_Pin_0);//低电平点亮
	//GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_RESET);//RESET点亮，SET熄灭

	while(1)
	{
		GPIO_Write(GPIOA, ~0x0001);//对应二进制为0000 0000 0000 0001分别对应PA0~PA15端口,为电平点亮，所以为只第一个LED点亮
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0002);//对应二进制为0000 0000 0000 0010
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0004);//对应二进制为0000 0000 0000 0100
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0008);//对应二进制为0000 0000 0000 1000
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0010);//对应二进制为0000 0000 0001 0000
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0020);//对应二进制为0000 0000 0010 0000
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0040);//对应二进制为0000 0000 0100 0000
		Delay_ms(50);
		GPIO_Write(GPIOA, ~0x0080);//对应二进制为0000 0000 1000 0000
		Delay_ms(50);
	}

}
