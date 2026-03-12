#include "motor.h"
#include "pwm.h"


void set_motor_output(int pwm1,int pwm2)
{
	if(pwm1 >= 0)
	{
		//set_pwm(pwm);
        TIM_SetCompare2(TIM3,pwm1);
        TIM_SetCompare1(TIM3,0);
		//set_clockwise_rotate();
	}
	else if(pwm1 < 0)
	{
		//set_pwm(-pwm);
        TIM_SetCompare2(TIM3,0);
        TIM_SetCompare1(TIM3,-pwm1);
		//set_anticlockwise_rotate();
	}
	else
	{
    TIM_SetCompare2(TIM3,0);
    TIM_SetCompare1(TIM3,0);  	
		//set_stop_rotate();
	}
    
    if(pwm2 >= 0)
	{
		//set_pwm(pwm);
        TIM_SetCompare3(TIM3,pwm2);
        TIM_SetCompare4(TIM3,0);
		//set_clockwise_rotate();
	}
	else if(pwm2 < 0)
	{
		//set_pwm(-pwm);
        TIM_SetCompare3(TIM3,0);
        TIM_SetCompare4(TIM3,-pwm2);
		//set_anticlockwise_rotate();
	}
	else
	{
	TIM_SetCompare3(TIM3,0);
    TIM_SetCompare4(TIM3,0);
		//set_stop_rotate();
	}
}

