#include "stm32f10x.h"                  // Device header
#include "Delay.h"                  // Device header
#include "LED.h"
#include "Key.h"
#include "OLED.h"
#include "Servo.h"
#include "Serial.h"
#include "timer.h"
#include "Move.h"
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

//Servo_SetAngle_up(Init_Angle_up);
//Delay_ms(500);
//Servo_SetAngle_down(Init_Angle_down);
//Delay_ms(500);

float k = 0.00008;
float i = 0.0;
float d = 0.0;
float x_set = 0;//下方云台目标值，chat解释为
float y_set = 0;//上方云台

float k_laser = 0.00012;
float i_laser = 0.0;
float d_laser = 0.0;
int main(void)
{
	OLED_Init ();
	Servo_Init();
	Key_Init();
	Serial_Init();//串口初始化

//	OLED_ShowString(1, 1, "L");
//	OLED_ShowNum(1, 2, 160, 3);
//	OLED_ShowNum(1, 6, 119, 3);
//	
//	OLED_ShowString(2, 1, "R");//第二排
//	OLED_ShowNum(2, 2, 109, 3);
//	OLED_ShowNum(2, 6, 148, 3);
//	OLED_ShowString(2, 9, ",");
//	OLED_ShowNum(2, 10, 228, 3);
//	OLED_ShowNum(2, 14, 151, 3);
//	
//	OLED_ShowNum(3, 2, 229, 3);//第三排
//	OLED_ShowNum(3, 6, 67, 3);
//	OLED_ShowString(3, 9, ",");
//	OLED_ShowNum(3, 10, 112, 3);
//	OLED_ShowNum(3, 14, 67, 3);
	

	while(1)
	{
	    KeyNum = Key_GetNum();//这里用于得到key1(PB13)(=1)或者key2(PB14)(=2)的值
	    updatePoints();
	    //此仅仅为显示部分
		if (Serial_GetRxFlag() == 1) // 如果接收到数据包就在OLED上显示激光点和矩形角点坐标
        {
			OLED_Clear();
			//显示激光点的坐标
			OLED_ShowNum(1, 2, a, 3);
			OLED_ShowNum(1, 6, b, 3);
			//显示矩形角点坐标
            OLED_ShowNum(2, 2, x1, 3);
            OLED_ShowNum(2, 6, y1, 3);
            OLED_ShowNum(2, 10, x2, 3);
            OLED_ShowNum(2, 13, y2, 3);
            OLED_ShowNum(3, 2, x3, 3);
            OLED_ShowNum(3, 6, y3, 3);
            OLED_ShowNum(3, 10, x4, 3);
            OLED_ShowNum(3, 13, y4, 3);
//        }
        //如果key1按下,就只需使用矩形角点坐标，绕黑线环绕一圈模式
			if(KeyNum == 1)
			{
				set_pid_pos_param(&Pid_steer, k, i, d, x_set);//调节矩形的kid值
				set_pid_pos_param(&Pid_steer_y, k, i, d, y_set);

				int flag = 1;//表示需要开始向第一或是第二三四个点运动标志
				//表示到达第一个点左右附近
				while(x_er1 > 7 || y_er1 > 7)//||表示或，都为假时才会停止whlie循环
				{
					updatePoints();
					steer_to_track(1500, flag);//每运行一次，距离目标点更近一步，这里需要使用第一个点的偏差值
				}

				flag = 2;
				
				if(flag == 2)//需要向第二点运动了，需要使用第二点的偏差值
				{
					updatePoints();
					while(x_er2 > 7 || y_er2 > 7)//||表示或，表示到达第一个点左右附近
					{
						updatePoints();
						steer_to_track(1500, flag);
					}
					flag = 3;	
				}
				
				if(flag == 3)
				{
					updatePoints();
					while(x_er3 > 7 || y_er3 > 7)
					{
						updatePoints();
						steer_to_track(1500, flag);
					}
					flag = 4;	
				}

				if(flag == 4)
				{
					updatePoints();
					while(x_er4 > 7 || y_er4 > 7)//||表示或，表示到达第一个点左右附近
					{
						updatePoints();
						steer_to_track(1500, flag);
					}
				}
				
			}
			
			if(KeyNum == 2)//当按下key2时开始追踪激光点
			{
				set_pid_pos_param(&Pid_steer, k_laser, i_laser, d_laser, x_set);//调节矩形的kid值
				set_pid_pos_param(&Pid_steer_y, k_laser, i_laser, d_laser, y_set);
				
				update_L_Points();
				while(x0_err > 5 || y0_err > 5)//表示追踪到绿色激光点
				{
					update_L_Points();
					steer_to_track(1500, 5);
				}
			}
		}

	}//-----------------主循环------------------------------
}









