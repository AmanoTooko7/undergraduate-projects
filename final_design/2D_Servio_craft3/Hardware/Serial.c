#include "stm32f10x.h"                  // Device header
#include <stdio.h>
#include <stdarg.h>


uint8_t Serial_TxPacket[4];	
uint8_t Serial_RxFlag;     // 接收数据包标志位


/**
  * 函    数：串口初始化
  * 参    数：无
  * 返 回 值：无
  */
void Serial_Init(void)
{
	/*开启时钟*/
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);	//开启USART1的时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	//开启GPIOA的时钟
	
	/*GPIO初始化*/
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;//PA9为TX
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);					//将PA9引脚初始化为复用推挽输出
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;//由引脚定义表PA10为RX
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);					//将PA10引脚初始化为上拉输入
	
	/*USART初始化*/
	USART_InitTypeDef USART_InitStructure;					//定义结构体变量
	USART_InitStructure.USART_BaudRate = 9600;				//波特率
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;	//硬件流控制，不需要
	USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;	//模式，发送模式和接收模式均选择
	USART_InitStructure.USART_Parity = USART_Parity_No;		//奇偶校验，不需要
	USART_InitStructure.USART_StopBits = USART_StopBits_1;	//停止位，选择1位
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;		//字长，选择8位
	USART_Init(USART1, &USART_InitStructure);				//将结构体变量交给USART_Init，配置USART1
	
	/*中断输出配置*/
	USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);			//开启串口接收数据的中断
	
	/*NVIC中断分组*/
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);			//配置NVIC为分组2
	
	/*NVIC配置*/
	NVIC_InitTypeDef NVIC_InitStructure;					//定义结构体变量
	NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;		//选择配置NVIC的USART1线
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//指定NVIC线路使能
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;		//指定NVIC线路的抢占优先级为1
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;		//指定NVIC线路的响应优先级为1
	NVIC_Init(&NVIC_InitStructure);							//将结构体变量交给NVIC_Init，配置NVIC外设
	
	/*USART使能*/
	USART_Cmd(USART1, ENABLE);								//使能USART1，串口开始运行
}


/**
  * 函    数：串口发送一个字节
  * 参    数：Byte 要发送的一个字节
  * 返 回 值：无
  */
void Serial_SendByte(uint8_t Byte)
{
	USART_SendData(USART1, Byte);		//将字节数据写入数据寄存器，写入后USART自动生成时序波形
	while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);	//等待发送完成
	/*下次写入数据寄存器会自动清除发送完成标志位，故此循环后，无需清除标志位*/
}

/**
  * 函    数：串口发送一个数组
  * 参    数：Array 要发送数组的首地址
  * 参    数：Length 要发送数组的长度
  * 返 回 值：无
  */
void Serial_SendArray(uint8_t *Array, uint16_t Length)
{
	uint16_t i;
	for (i = 0; i < Length; i ++)		//遍历数组
	{
		Serial_SendByte(Array[i]);		//依次调用Serial_SendByte发送每个字节数据
	}
}

/**
  * 函    数：串口发送一个字符串
  * 参    数：String 要发送字符串的首地址
  * 返 回 值：无
  */
void Serial_SendString(char *String)
{
	uint8_t i;
	for (i = 0; String[i] != '\0'; i ++)//遍历字符数组（字符串），遇到字符串结束标志位后停止
	{
		Serial_SendByte(String[i]);		//依次调用Serial_SendByte发送每个字节数据
	}
}

/**
  * 函    数：次方函数（内部使用）
  * 返 回 值：返回值等于X的Y次方
  */
uint32_t Serial_Pow(uint32_t X, uint32_t Y)
{
	uint32_t Result = 1;	//设置结果初值为1
	while (Y --)			//执行Y次
	{
		Result *= X;		//将X累乘到结果
	}
	return Result;
}

/**
  * 函    数：串口发送数字
  * 参    数：Number 要发送的数字，范围：0~4294967295
  * 参    数：Length 要发送数字的长度，范围：0~10
  * 返 回 值：无
  */
void Serial_SendNumber(uint32_t Number, uint8_t Length)
{
	uint8_t i;
	for (i = 0; i < Length; i ++)		//根据数字长度遍历数字的每一位
	{
		Serial_SendByte(Number / Serial_Pow(10, Length - i - 1) % 10 + '0');	//依次调用Serial_SendByte发送每位数字
	}
}

/**
  * 函    数：使用printf需要重定向的底层函数
  * 参    数：保持原始格式即可，无需变动
  * 返 回 值：保持原始格式即可，无需变动
  */
int fputc(int ch, FILE *f)
{
	Serial_SendByte(ch);			//将printf的底层重定向到自己的发送字节函数
	return ch;
}

/**
  * 函    数：自己封装的prinf函数
  * 参    数：format 格式化字符串
  * 参    数：... 可变的参数列表
  * 返 回 值：无
  */
void Serial_Printf(char *format, ...)
{
	char String[100];				//定义字符数组
	va_list arg;					//定义可变参数列表数据类型的变量arg
	va_start(arg, format);			//从format开始，接收参数列表到arg变量
	vsprintf(String, format, arg);	//使用vsprintf打印格式化字符串和参数列表到字符数组中
	va_end(arg);					//结束变量arg
	Serial_SendString(String);		//串口发送字符数组（字符串）
}

void Serial_SendPacket(void)
{
	Serial_SendByte(0xFF);
	Serial_SendArray(Serial_TxPacket, 4);
	Serial_SendByte(0xFE);
}

/**
  * 函    数：获取串口接收数据包标志位
  * 参    数：无
  * 返 回 值：串口接收数据包标志位，范围：0~1，接收到数据包后，标志位置1，读取后标志位自动清零
  */
uint8_t Serial_GetRxFlag(void)
{
	if (Serial_RxFlag == 1)			//如果标志位为1
	{
		Serial_RxFlag = 0;
		return 1;					//则返回1，并自动清零标志位
	}
	return 0;						//如果标志位为0，则返回0
}




uint8_t rx_buffer[100];
void USART1_IRQHandler(void)
{
	
	 static uint32_t rx_index = 0;      //接受到的数据包中的数据个数
	 static uint8_t rx_state = 0;       //此状态表示总状态
	 static uint8_t rect_rx_state = 0;  //接收的数据状态(矩形的)
	 static uint8_t laser_rx_state = 0; //接收的数据状态(激光点)
//	 static uint8_t 
	
	 if (USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)// 读取接收缓冲区的数据
	 {
		 uint8_t RxData = USART_ReceiveData(USART1);//接受到数据
		
		 if (rx_state == 0)//接到数据前的初始化------------------------------------------------------
		 {
			 if (RxData ==  '@')//如果到了接收矩形角点数据的初始状态且检测到了包头
			 {
				Serial_RxFlag=1;//测试--------------
				rect_rx_state = 1;
                rx_index = 0;
				rx_state = 1;
			 }
			 
			 else if (RxData == '!')//表示接收到了激光点的数据包包头
			 {
				 laser_rx_state = 1;
				 rx_index = 0;
				 rx_state = 1;
			 }
			
		 }
		 if (rx_state == 1)//表示接受到任意一种数据包--------------------------------------------
		 {
			 rx_buffer[rx_index++] = RxData;
			 if(rx_index == 34)  //如果是矩形数据包，包括包头包尾共34位
			 {
				 rect_rx_state = 2; //置收到矩形长度的数据包状态为2
			 }
			 else if(rx_index == 6)    //置收到激光点长度的数据包状态为2
			 {
				laser_rx_state =  2;
			 }
		 }
		 
		 if (rect_rx_state == 2)//如果到达接收(矩形)数据末状态----------------------------------
		 {
			 if (RxData == '%')//且收到了矩形的包尾
			 {
				 OLED_ShowNum(2, 2, rx_buffer[0], 3);
				 rect_rx_state = 0;
				 rx_index = 0;
				 rx_state = 0;
				 Serial_RxFlag = 1;		//接收数据包标志位置1，成功接收一个数据包
			 }
			 else //如果不是包尾
			 {
				 rect_rx_state = 0;
			 }
		 }
		 if(laser_rx_state == 2)//如果到达接收(激光)数据末状态----------------------------------
		 {
			 if (RxData == '#')
			 {
				 parse_laser(rx_buffer);
				 laser_rx_state = 0;
				 rx_index = 0;
				 rx_state = 0;
				 Serial_RxFlag = 1;
			 }
			 else
			 {
				 laser_rx_state = 0;
			 }
		 }
		USART_ClearITPendingBit(USART1, USART_IT_RXNE);		//清除标志位
	 }
}

uint32_t x1, y1, x2, y2, x3, y3, x4, y4;//矩形的四个角点
uint32_t a, b;//回传的激光点坐标

//这个函数解析来自OpenMV回传的b'!\xa0\x00\x00\x00s\x00\x00\x00#'数据包
void parse_laser(uint8_t* rx_buffer)
{
	if (rx_buffer == NULL)// 如果缓冲区为空，则退出函数
    {
        return;
    }
 // 提取坐标数据并转换为十进制
    uint8_t x_high = rx_buffer[1];
    uint8_t x_low = rx_buffer[2];
    uint8_t y_high = rx_buffer[3];
    uint8_t y_low = rx_buffer[4];

    // 转换为十进制
    uint16_t x_coordinate = (x_high * 256) + x_low;
    uint16_t y_coordinate = (y_high * 256) + y_low;

    // 存储到全局变量中
    a = x_coordinate;
    b = y_coordinate;
}

//此函数解析 b'@\x93\x00\x00\x00\xc8\x00\x00\x00\r\x01\x00\x00\xcb\x00\x00\x00\r\x01\x00\x00v\x00\x00\x00\x96\x00\x00\x00u\x00\x00\x00#'这种数据包
void parse_rect(uint8_t* rx_buffer)//解析矩形的数据包函数
{
    if (rx_buffer == NULL)// 如果缓冲区为空，则退出函数
    {
        return;
    }
    
    uint32_t integers[8];//定义八个整数的数组
    
    // 从第一个数据开始解析，跳过包头 '@'
    for (int i =1; i<=8; i++)
    {
        integers[i-1] = (rx_buffer[i*4] << 24 |
                         rx_buffer[i*4 + 1] << 16 |
                         rx_buffer[i*4 + 2]  << 8 |
                         rx_buffer[i*4 + 3] );
    }
    
    
    //x1,x2,x3,x4的范围值在0到320，y1,y2,y3,y4的值在0到240
    if (integers[0] >= 0 && integers[0] <= 320 &&
        integers[1] >= 0 && integers[1] <= 240 &&
        integers[2] >= 0 && integers[2] <= 320 &&
        integers[3] >= 0 && integers[3] <= 240 &&
        integers[4] >= 0 && integers[4] <= 320 &&
        integers[5] >= 0 && integers[5] <= 240 &&
        integers[6] >= 0 && integers[6] <= 320 &&
        integers[7] >= 0 && integers[7] <= 240)
    {
        // 如果所有坐标值都在范围内，则将解析后的坐标值赋值给全局变量
        x1 = integers[0];
        y1 = integers[1];
        x2 = integers[2];
        y2 = integers[3];
        x3 = integers[4];
        y3 = integers[5];
        x4 = integers[6];
        y4 = integers[7];
    }
    else//如果在这有任意一个x和y值在范围值以外则舍弃这个数据包，接收下一个数据包
    {

    }
}


