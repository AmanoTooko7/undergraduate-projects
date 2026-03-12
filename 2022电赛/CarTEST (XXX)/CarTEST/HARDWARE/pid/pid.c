#include "pid.h"


pid_handle_t servo_pid = {SERVO_RHO_KP,SERVO_RHO_KI,SERVO_RHO_KD,SERVO_THETA_KP,SERVO_THETA_KI,SERVO_THETA_KD};
pid_handle_t motor_pid = {MOTOR_RHO_KP,MOTOR_RHO_KI,MOTOR_RHO_KD,MOTOR_THETA_KP,MOTOR_THETA_KI,MOTOR_THETA_KD};

float rho_error;
float rho_last_error;
double rho_error_sum;


float theta_error;
float theta_last_error;
double theta_error_sum;

float motor_out = 0;
/*
	目标速度 - 实际速度 = error
*/
//static float get_pid_t(pid_t *pid,float error)
//{
//	float output = 0;
//	pid->error = error;	
//	output = pid->error * pid->KP + pid->error_sum * pid->KI + pid->KD * (pid->error - pid->last_error);
//	pid->error_sum += pid->error;
//	pid->last_error = pid->error;
//	return output;
//}

//float get_pid(pid_handle_t *pid,float pho_err,float theta_err)
//{
//	return get_pid_t(&pid->rho,pho_err) + get_pid_t(&pid->theta,theta_err);
//}



static float SERVO_PD_t(pid_t *pid,float error,float last_error)
{	
	float output = pid->KP * error + pid->KD * (error - last_error);

	//error_sum += error;
	
	
	if(output >= 30)
		output = 30;
	else if(output <= -30)
		output = -30;
	
	return output;
}

float SERVO_PD(pid_handle_t *pid)
{
	float output = SERVO_PD_t(&pid->rho,rho_error,rho_last_error) + SERVO_PD_t(&pid->theta,theta_error,theta_last_error);
	
	
	
	if(output >= 30)
		output = 30;
	else if(output <= -30)
		output = -30;	
	
	return output;	
}


//增量式PI
float MOTOR_PI_t(pid_t *pid,float error,float last_error)
{
	float output =  pid->KP * (error - last_error) + pid->KI * error;
	last_error = error;
	if(output < 0)
		output = -output;
	return output;
}


float MOTOR_PI(pid_handle_t *pid)
{
	float output = MOTOR_PI_t(&pid->rho,rho_error,rho_last_error) + MOTOR_PI_t(&pid->theta,theta_error,theta_last_error);
	rho_last_error = rho_error;
	theta_last_error = theta_error;
	if(output >= 100)
	{
		output = 100;
	}
	return output;
}
