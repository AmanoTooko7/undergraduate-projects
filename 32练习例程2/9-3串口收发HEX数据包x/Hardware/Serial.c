#include "stm32f10x.h"                  // Device header
#include <stdio.h>
#include <stdarg.h>

uint8_t Serial_TxPacket[4];//这两排只存储发送和接受的载荷数据，包头包尾不存
uint8_t Serial_RxPacket[4];
uint8_t Serial_RxFlag;

/*
1.开启USART和GPIO的时钟
2.GPIO初始化，把TX配置成复用输出。RX配置成输入
3.配置USART,使用结构体配置
4.只发送数据的功能就只需开启USART。若要接收数据那就在开启USART之前。再加ITConfig和NVIC的代码
*/
/*
本程序还加上了使用中断的方法32接收数据
*/

void Serial_Init(void){
	//1
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	//2
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;//将PA9配置为复用推挽输出GPIO_Mode_AF_PP
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;//PA9为TX
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
													
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;//上拉输入
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;//由引脚定义表PA10为RX
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	//3
	USART_InitTypeDef USART_InitStructure;
	USART_InitStructure.USART_BaudRate = 9600;//配置比特率
	USART_InitStructure.USART_WordLength = USART_WordLength_9b;//字长选择，因为不需要校验所以选择8位字长
	USART_InitStructure.USART_StopBits = USART_StopBits_1; //选择一位停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//选择无校验
	USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;//配置串口模式，将PA9配置为传输模式,PA10为接收模式
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//硬件流控配置，这里不使用
	USART_Init(USART1, &USART_InitStructure);
	//4开启USART
	
	USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);//表示当USART1接受到数据时，将会产生接收中断,开启RXNE标志位到NVIC的输出
	
	//以下为NVIC优先权分组,
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	
	//初始化NVIC的USART1
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;//使用USART1为中断
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;//中断优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure);
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


//调用此函数，TxPacket数组的四个数据就会自动加上包头包尾发送出去、
void Serial_SendPacket(void){
	Serial_SendByte(0xFF);					//发送包头
	Serial_SendArray(Serial_TxPacket, 4);	//发送数据
	Serial_SendByte(0xFE);					//发送包尾

}


//中断
uint8_t Serial_GetRxFlag(void){//清除接受到的数据的标志位
	if (Serial_RxFlag == 1){
		Serial_RxFlag = 0;
		return 1;
	}
	return 0;
}

//此函数用于
void USART1_IRQHandler(void){//USART1产生中断固定的函数名称
	
	static uint8_t RxState = 0;        //状态变量，见pptHEX数据包接收，有=0为等待包头，=1为接收数据，=2为等待包尾三个状态
	static uint8_t pRxPacket = 0;;//表示接收到的数据接收到哪一个了

	if (USART_GetITStatus(USART1, USART_IT_RXNE) == SET){//表示如果USART1接收到数据		
		
		uint8_t RxData = USART_ReceiveData(USART1);//接收来自USART1的数据		
		
		if (RxState == 0)
		{
			if(RxData == 0xFF)//表示接收到数据头
				{
					RxState = 1;//接收到数据头就转移到下一个状态
					pRxPacket = 0;//数据包的位置归零
				}
		}
		
		else if(RxState == 1){//表示接收到数据
			Serial_RxPacket[pRxPacket] = RxData;   //将数据存入数据包数组的指定位置
			pRxPacket ++;
			if(pRxPacket >=4)      //如果收够4个数据
			{
				RxState = 2;	   //就转移到下一个标志位	
			}
		}
		
		else if(RxState == 2)    //表示到达数据包包尾
		{
			if(RxData == 0xFE)	   //表示接收数据包包尾
			{
				RxState = 0;
				Serial_RxFlag = 1;	  //接收数据包标志位置1，成功接收一个数据包
			}
		}
		
		USART_ClearITPendingBit(USART1, USART_IT_RXNE);//清除USART的USART_IT_RXNE的标志位
	}
}



