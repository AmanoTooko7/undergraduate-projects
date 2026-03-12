#include "stm32f10x.h"
#include "Delay.h"
#include "OLED.h"

int main (void)
{
	OLED_Init();
	
  Serial_Init();
	
//	Serial_SendByte();   											//发送字节
//	uint8_t MyArray[]={0x42,0x43,0x44,0x45};  //发送数组
//	Serial_SendArray(MyArray,4);							//发送数组
//	Serial_SendString("hellow");        		  //发送字符串
//	Serial_SendNumber(12345,5);       				//发送数字
	
//	printf("Num=%d\n\r",666);
	 
//	char String[100];
//	sprintf(String,"Num=%d\n\r",666);
//	Serial_SendString(String);
	
	Serial_Printf("Num=%d\n\r",666,234);
	
	
	while(1)
		
	{
		

	}
		

}