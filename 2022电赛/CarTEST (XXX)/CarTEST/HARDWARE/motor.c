#include "motor.h"


void set_motor_output(int pwm1,int pwm2,int pwm3,int pwm4)
{
    TIM2->CCR1 = pwm1;
    TIM2->CCR2 = pwm2;
    TIM2->CCR3 = pwm3;
    TIM2->CCR4 = pwm4;
    TIM1->CCR1 = 0;
    TIM3->CCR4 = 0;
}
void set_zhuanwan_output(int pwm)
{    
    TIM3->CCR2 = 214+pwm;

}
void start_motor(void)
{
    stop_flag=0;
    start_flag=1;
}
void stop_motor(void)
{
    stop_flag=1;
    start_flag=0;
    TIM2->CCR1 = 0;
    TIM2->CCR2 = 0;
    TIM2->CCR3 = 0;
    TIM2->CCR4 = 0;
    TIM1->CCR1 = 0;
    TIM1->CCR4 = 0;
}
void ABS_motor(int pwm1,int pwm2)
{
     TIM1->CCR1 = pwm1;
     TIM1->CCR4 = pwm2;
      //abs_flag=1;
    HAL_Delay(150);
    TIM1->CCR1 = 0;
    TIM1->CCR4 = 0;
}
