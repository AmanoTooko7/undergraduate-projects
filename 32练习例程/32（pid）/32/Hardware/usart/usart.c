#include "sys.h"
#include "usart.h"	
#include "protocol.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


////////////////////////////////////////////////////////////////////////////////// 	 
//如果使用ucos,则包括下面的头文件即可.
#if SYSTEM_SUPPORT_OS
#include "includes.h"					//ucos 使用	  
#endif
 

//////////////////////////////////////////////////////////////////
//加入以下代码,支持printf函数,而不需要选择use MicroLIB	  
#if 1
#pragma import(__use_no_semihosting)             
//标准库需要的支持函数                 
struct __FILE 
{ 
	int handle; 
}; 

FILE __stdout;       
//定义_sys_exit()以避免使用半主机模式    
_sys_exit(int x) 
{ 
	x = x; 
} 
//重定义fputc函数 
int fputc(int ch, FILE *f)
{ 	
	while((usart_x->SR&0X40)==0);//循环发送,直到发送完毕   
	usart_x->DR = (u8) ch;      
	return ch;
}
#endif
 
#if EN_USART1_RX   //如果使能了接收
//串口1中断服务程序
//注意,读取USARTx->SR能避免莫名其妙的错误   	
u8 USART_RX_BUF[USART_REC_LEN];     //接收缓冲,最大USART_REC_LEN个字节.
//接收状态
//bit15，	接收完成标志
//bit14，	接收到0x0d
//bit13~0，	接收到的有效字节数目
u16 USART_RX_STA=0;       //接收状态标记	



//初始化IO 串口1 
//bound:波特率
void uart_init(u32 bound)
{
	//GPIO端口设置
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE); //使能GPIOA时钟
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2,ENABLE);//使能USART1时钟

	//串口1对应引脚复用映射
//	GPIO_PinAFConfig(GPIOA,GPIO_PinSource9,GPIO_AF_USART1); //GPIOA9复用为USART1
//	GPIO_PinAFConfig(GPIOA,GPIO_PinSource10,GPIO_AF_USART1); //GPIOA10复用为USART1

	//USART1端口配置
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3; //设置USART2的RX接口是PA3
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;//浮空输入
    GPIO_Init(GPIOA, &GPIO_InitStructure); 

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2; //设置USART2的TX接口是PA2
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;	//复用推挽输出
    GPIO_Init(GPIOA, &GPIO_InitStructure);  

	//USART1 初始化设置
	USART_InitStructure.USART_BaudRate = bound;//波特率设置
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式
	USART_Init(usart_x, &USART_InitStructure); //初始化串口1

	USART_Cmd(usart_x, ENABLE);  //使能串口1 
	
	//USART_ClearFlag(USART1, USART_FLAG_TC);
	
#if EN_USART1_RX	
	USART_ITConfig(usart_x, USART_IT_RXNE, ENABLE);//开启相关中断
	//USART_ITConfig(USART2, USART_IT_IDLE, ENABLE);

	//Usart1 NVIC 配置
    //NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);
	NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;//串口1中断通道
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3;//抢占优先级3
	NVIC_InitStructure.NVIC_IRQChannelSubPriority =3;		//子优先级3
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
	NVIC_Init(&NVIC_InitStructure);	//根据指定的参数初始化VIC寄存器、

#endif
	
}


void usart1_send(u8*data, u8 len)
{
	u8 i;
    // PCout(13)=~PCout(13);              
	for(i=0;i<len;i++)
	{
		while(USART_GetFlagStatus(usart_x,USART_FLAG_TC)==RESET); 
		USART_SendData(usart_x,data[i]);   
	}
}

//=======================================
//串口1中断服务程序
//=======================================
uint8_t Recv1[128]={0};//串口接收缓存
u8 rx_cnt=0;//接收数据个数计数变量

int sizecopy=128;

void USART2_IRQHandler(void)                	
{
	uint8_t data;//接收数据暂存变量
	uint8_t bufcopy[128];//最多只取前64个数据
    

	if(USART_GetITStatus(usart_x, USART_IT_RXNE) != RESET)  //接收中断
	{
		data = USART_ReceiveData(usart_x);   			
		Recv1[rx_cnt++]=data;//接收的数据存入接收数组 
		protocol_data_recv(&data, 1);
		
		USART_ClearITPendingBit(usart_x,USART_IT_RXNE);
	} 
	
	if(USART_GetITStatus(usart_x, USART_IT_IDLE) != RESET)//空闲中断
	{
		data = usart_x->SR;//串口空闲中断的中断标志只能通过先读SR寄存器，再读DR寄存器清除！
		data = usart_x->DR;
		
		//清空本地接收数组
		memset(bufcopy,0,sizecopy);
		
		memcpy(bufcopy,Recv1,rx_cnt);//有几个复制几个
		
		protocol_data_recv(bufcopy, rx_cnt);

		memset(Recv1,0,sizecopy);
		rx_cnt=0;
	}
} 

#endif	

 



