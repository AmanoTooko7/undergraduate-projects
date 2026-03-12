#ifndef __PID_H_
#define __PID_H_

#include "main.h"

#define SERVO_BASIC_P	0.03

#define SERVO_RHO_KP	1.5
#define SERVO_RHO_KI	0
#define SERVO_RHO_KD	0.4

#define SERVO_THETA_KP	0.5
#define SERVO_THETA_KI	0
#define SERVO_THETA_KD	0.1


#define MOTOR_RHO_KP	10
#define MOTOR_RHO_KI	12
#define MOTOR_RHO_KD	0

#define MOTOR_THETA_KP	7	 
#define MOTOR_THETA_KI	7
#define MOTOR_THETA_KD	0

typedef struct 
{
	float KP;
	float KI;
	float KD;	
}pid_t;

typedef struct
{
	pid_t rho;
	pid_t theta;
}pid_handle_t;

extern pid_handle_t servo_pid;
extern pid_handle_t motor_pid;

extern float rho_error;
extern float rho_last_error;
extern double rho_error_sum;


extern float theta_error;
extern float theta_last_error;
extern double theta_error_sum;



float SERVO_PD(pid_handle_t *pid);
float MOTOR_PI(pid_handle_t *pid);

#endif /* __PID_H_ */


