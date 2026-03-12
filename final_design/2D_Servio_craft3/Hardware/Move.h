#ifndef __MOVE_H
#define __MOVE_H

#include <stdio.h>

typedef struct{
    float Sv;//设定值
    float EK;//当前误差
    float SUM_EK;//误差累加
    float OUT;//控制器的输出
    float Kp;//比例系数
    float Ki;//积分系数
    float Kd;//微分系数
    float EK_NEXT;//下一次的误差
}PID_POS;

//Points_t表示矩形的四个点，Point表示每个点的x,y坐标
typedef struct{
	uint32_t x;
	uint32_t y;
}Point;

typedef struct{
	Point point1;  //定义一个名为Point的Point成员
	Point point2;
	Point point3;
	Point point4;
}Points_t;

typedef struct{    //
	uint32_t a0;
	uint32_t b0;
}Laser_dot;

extern Points_t Points;
extern int x_er1, y_er1, x_er2, y_er2, x_er3, y_er3, x_er4, y_er4;//这是与矩形的误差
extern int x0_err, y0_err;//这是红色激光点与绿色激光点的误差
extern PID_POS Pid_steer;
extern PID_POS Pid_steer_y;
extern int x0, y0;

void updatePoints(void);//每使用一次更新矩形角点数据
void update_L_Points(void);//更新激光点坐标
float Servo_Move_PID(PID_POS *pid_pos, float actual_data);
void set_pid_pos_param(PID_POS *pid_pos, float p, float i, float d, float sv);
void steer_to_track(int angle, int flag);
float adjust_pid_output(float pid_steer_out, float pid_output);

#endif
