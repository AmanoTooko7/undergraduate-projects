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
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);//用的PB12为蜂鸣器的io口输出
	
    GPIO_InitTypeDef GPIO_InitStructure;  //这是结构体名字叫GPIO_InitTypeDef有GPIO_Mode,GPIO_Pin,GPIO_Speed三种类型
	//下三排作用为：GPIOA外设，0号引脚，配置为推挽输出(pp)，50MHz的速度
	//推挽输出高低电平都有驱动能力，
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); 
	
	//GPIO_SetBits(GPIOA, GPIO_Pin_0);
	//GPIO_ResetBits(GPIOA, GPIO_Pin_0);//低电平点亮
	//GPIO_WriteBit(GPIOA, GPIO_Pin_0, Bit_RESET);//RESET点亮，SET熄灭

	while(1)
	{
		GPIO_ResetBits(GPIOB, GPIO_Pin_12);//响500ms后关闭
		Delay_ms(500);
		GPIO_SetBits(GPIOB, GPIO_Pin_12);
		Delay_ms(500);
	}

}
