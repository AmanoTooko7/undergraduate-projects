#include "stm32f10x.h"                  // Device header
#include "Serial.h"
#include "Move.h"
#include "Servo.h"
#include "pwm.h"
#include <math.h>

//在来自https://www.guyuehome.com/45936修改
//红色激光点L(160,119)，本文件为了两个效果
//一是得到矩形坐标后，计算L与点1差值

int x0 = 160;
int y0 = 119;

PID_POS Pid_steer, Pid_steer_y;    //设置两个结构体存储x,y轴舵机的PID参数值
Points_t Points; 				   //定义一个名为Points的结构体
Laser_dot LaserDot;
/*以下程序为来自串口通信函数接收的
x1,y1,x2,y2,x3,y3,x4,y4八个数据
每使用一次里面的8个数据就更新一次
若单独使用例 uint32_t x1 = points.point1.x;
			 uint32_t y1 = points.point1.y;
*/
void updatePoints(void) {
    Points.point1.x = x1;
    Points.point1.y = y1;
    Points.point2.x = x2;
    Points.point2.y = y2;
    Points.point3.x = x3;
    Points.point3.y = y3;
    Points.point4.x = x4;
    Points.point4.y = y4;
}

void update_L_Points(void){
	LaserDot.a0 = a;
	LaserDot.b0 = b;
}

//此仅仅是输入输出PID控制器的输出量，真正的增量式PID工作在steer_to_track()
float Servo_Move_PID(PID_POS *pid_pos, float actual_data)
{
    pid_pos->EK = pid_pos->Sv - actual_data; // 计算当前误差,当到达Sv时
    pid_pos->SUM_EK += pid_pos->EK;          // 误差的累积

    pid_pos->OUT =
		pid_pos->Kp * pid_pos->EK +           // 当前误差
		pid_pos->Ki * pid_pos->SUM_EK +       // 累积的误差
		pid_pos->Kd * (pid_pos->EK - pid_pos->EK_NEXT); // 当前误差与上一次的误差的差值

    return pid_pos->OUT;
}

//下面这个函数用于直接设定Kp,Ki,Kd，和目标值Sv
void set_pid_pos_param(PID_POS *pid_pos,float p,float i,float d,float sv)
{
    pid_pos->Kp=p;
    pid_pos->Ki=i;
    pid_pos->Kd=d;
    pid_pos->Sv=sv;
}

//接收历史控制量和pid的输出量
//作用是调整舵机的输出值，限制在500-2000之内
float adjust_pid_output(float pid_steer_out, float pid_output) {
    pid_steer_out += pid_output;
    if(pid_steer_out >= 2000)         //舵机角度限幅，以防转多了卡住
       pid_steer_out = 2000;
    if(pid_steer_out < 500)
       pid_steer_out = 500;
    return pid_steer_out;
}


//定义8个误差变量计算OPENMV传送过来矩形的坐标偏差值,设置为全局变量以便主循环能访问
int x_er1=0, y_er1=0, x_er2=0, y_er2=0, x_er3=0, y_er3=0, x_er4=0, y_er4=0;
int x0_err=0, y0_err=0;//初始化与绿色激光点的偏差值
//此函数目的是给定初始角度，根据OpenMV回传的坐标值，将上下两个舵机转动到指定的角度x_set,y_set
void steer_to_track(int angle, int flag) //输入角度为舵机的初始角度
{
    static float pid_steer_out=0; 		//X轴PID输出量
    static float pid_steer_out_y=0; 	//Y轴PID输出量
    static int pid_outputs[8];				//用于储存8个数据的PID输出量
    updatePoints();
	
	int x_err[4], y_err[4];
	Point points[4] = {Points.point1, Points.point2, Points.point3, Points.point4};

	for (int i = 0; i < 4; i++) {
		x_err[i] = points[i].x - x0;
		y_err[i] = points[i].y - y0;
		pid_outputs[i] = Servo_Move_PID(&Pid_steer, x_err[i]);
		pid_outputs[i+4] = Servo_Move_PID(&Pid_steer_y, y_err[i]);
	}

	x0_err = a - x0;
	y0_err = b - y0;
	
	
//	x_er1 = Points.point1.x - x0 ;//第一个点与红色激光点误差
//    y_er1 = Points.point1.y - y0 ;//
//	x_er2 = Points.point2.x - x0 ;//第二个点与红色激光点误差
//    y_er2 = Points.point2.y - y0 ;//
//	x_er3 = Points.point3.x - x0 ;//第三个点与红色激光点误差
//    y_er3 = Points.point3.y - y0;//
//	x_er4 = Points.point4.x - x0 ;//第四个点与红色激光点误差
//    y_er4 = Points.point4.y - y0 ;//

//	x0_err = a - x0;//与绿色激光点的误差
//	y0_err = b - y0;


//    //这里是将(第一点)X轴的偏差值传入PID控制器，得到第一点X轴的输出量赋值给PID的输出数组
//    //同理有四个点，所以有四个输出量，
//    pid_outputs[0] = Servo_Move_PID(&Pid_steer, x_er1);
//	pid_outputs[1] = Servo_Move_PID(&Pid_steer, x_er2);
//	pid_outputs[2] = Servo_Move_PID(&Pid_steer, x_er3);
//	pid_outputs[3] = Servo_Move_PID(&Pid_steer, x_er4);

//    pid_outputs[4] = Servo_Move_PID(&Pid_steer_y,y_er1);//这里是将Y轴的偏差值传入PID控制器，得到y轴的输出量
//	pid_outputs[5] = Servo_Move_PID(&Pid_steer_y,y_er2);
//	pid_outputs[6] = Servo_Move_PID(&Pid_steer_y,y_er3);
//    pid_outputs[7] = Servo_Move_PID(&Pid_steer_y,y_er4);


	//跟随矩形程序
	if(flag == 1){   //追踪第一个矩形角点
		pid_steer_out = adjust_pid_output(pid_steer_out, pid_outputs[0]);
		pid_steer_out_y = adjust_pid_output(pid_steer_out_y, pid_outputs[4]);
	}

	else if(flag == 2){   //追踪第二个矩形角点
        pid_steer_out = adjust_pid_output(pid_steer_out, pid_outputs[1]);
        pid_steer_out_y = adjust_pid_output(pid_steer_out_y, pid_outputs[5]);
	}
	else if(flag == 3){   //追踪第三个矩形角点
		pid_steer_out = adjust_pid_output(pid_steer_out, pid_outputs[2]);
		pid_steer_out_y = adjust_pid_output(pid_steer_out_y, pid_outputs[6]);
	}
	else if(flag == 4){   //追踪第四个矩形角点
		pid_steer_out = adjust_pid_output(pid_steer_out, pid_outputs[3]);
		pid_steer_out_y = adjust_pid_output(pid_steer_out_y, pid_outputs[7]);
	}
	else if(flag == 5){      //这是追踪绿色激光点
		pid_steer_out = adjust_pid_output(pid_steer_out, Servo_Move_PID(&Pid_steer, x0_err));
		pid_steer_out_y = adjust_pid_output(pid_steer_out_y, Servo_Move_PID(&Pid_steer_y, y0_err));
	}

//	if(flag == 1){
//		pid_steer_out += pid_outputs[0];
//		if(pid_steer_out >= 2000)         //舵机角度限幅，以防转多了卡住
//		   pid_steer_out = 2000;
//		if(pid_steer_out < 500)
//		   pid_steer_out = 500;
//		pid_steer_out += pid_outputs[4];
//		if(pid_steer_out_y >= 2000)   //舵机角度限幅
//		   pid_steer_out_y = 2000;
//		if(pid_steer_out_y <= 500)
//		   pid_steer_out_y = 500;
//	}
//	else if(flag == 2){
//		pid_steer_out += pid_outputs[1];
//		if(pid_steer_out >= 2000)         //舵机角度限幅，以防转多了卡住
//		   pid_steer_out = 2000;
//		if(pid_steer_out < 500)
//		   pid_steer_out = 500;
//		pid_steer_out += pid_outputs[5];
//		if(pid_steer_out_y >= 2000)   //舵机角度限幅
//		   pid_steer_out_y = 2000;
//		if(pid_steer_out_y <= 500)
//		   pid_steer_out_y = 500;
//	}
//	else if(flag == 3){
//		pid_steer_out += pid_outputs[2];
//		if(pid_steer_out >= 2000)         //舵机角度限幅，以防转多了卡住
//		   pid_steer_out = 2000;
//		if(pid_steer_out < 500)
//		   pid_steer_out = 500;
//		pid_steer_out += pid_outputs[6];
//		if(pid_steer_out_y >= 2000)   //舵机角度限幅
//		   pid_steer_out_y = 2000;
//		if(pid_steer_out_y <= 500)
//		   pid_steer_out_y = 500;
//	}
//	else if(flag == 4){
//		pid_steer_out += pid_outputs[3];
//		if(pid_steer_out >= 2000)         //舵机角度限幅，以防转多了卡住
//		   pid_steer_out = 2000;
//		if(pid_steer_out < 500)
//		   pid_steer_out = 500;
//		pid_steer_out += pid_outputs[7];
//		if(pid_steer_out_y >= 2000)   //舵机角度限幅
//		   pid_steer_out_y = 2000;
//		if(pid_steer_out_y <= 500)
//		   pid_steer_out_y = 500;
//	}
//	else if(flag == 5){      //这是追踪绿色激光点
//		pid_steer_out += Servo_Move_PID(&Pid_steer, x0_err);
//		if(pid_steer_out >= 2000)     
//		   pid_steer_out = 2000;
//		if(pid_steer_out < 500)
//		   pid_steer_out = 500;
//		pid_steer_out += Servo_Move_PID(&Pid_steer_y, y0_err);
//		if(pid_steer_out_y >= 2000) 
//		   pid_steer_out_y = 2000;
//		if(pid_steer_out_y <= 500)
//		   pid_steer_out_y = 500;
//	}

    TIM_SetCompare2(TIM2,(angle + pid_steer_out));
    TIM_SetCompare3(TIM2,(angle + pid_steer_out_y));
}

