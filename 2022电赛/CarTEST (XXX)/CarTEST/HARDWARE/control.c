#include "control.h"

float set_pwm=350;
char mode_flag=0;
char start_flag=0,stop_flag=0;

char exit_scanl=0,exit_scanr=0;
char mid_scan1_flag=0,mid_scan2_flag=0;
char process_flag=0;
char stop_5s_flag=0;
char stop_5s_flag_u=0;
char key_count=0;
char openmv_flag=0; 
    
char click_M(void)
{
    static char flag_key=1;//按键按松开标志
    if(flag_key&&HAL_GPIO_ReadPin(GPIOC,GPIO_PIN_13)==GPIO_PIN_RESET)
    {
    flag_key=0;
    return 1;	// 按键按下
    }
    else if(HAL_GPIO_ReadPin(GPIOC,GPIO_PIN_13)==GPIO_PIN_SET)	flag_key=1;
    return 0;//无按键按下
}
char click_STAR(void)
{
    static char flag_key=1;//按键按松开标志
    if(flag_key&&HAL_GPIO_ReadPin(GPIOB,GPIO_PIN_6)==GPIO_PIN_RESET)
    {
    flag_key=0;
    return 1;	// 按键按下
    }
    else if(HAL_GPIO_ReadPin(GPIOB,GPIO_PIN_6)==GPIO_PIN_SET)	flag_key=1;
    return 0;//无按键按下
}
void PROCESS_MOTOR(void)   //0.01s
{
    static uint16_t count=0;
        if(start_flag)
        {
			// 数据处理
			rho_error = (USART1_BUF[1] - 0x30) * 100 + (USART1_BUF[2] - 0x30) * 10 + (USART1_BUF[3] - 0x30);
			theta_error = (USART1_BUF[6] - 0x30) * 100 + (USART1_BUF[7] - 0x30) * 10 + (USART1_BUF[8] - 0x30);
           // openmv_flag=(USART1_BUF[10]-0x30)*10+(USART1_BUF[12]-0x30);  //11,10,01
			if(USART1_BUF[0] != '+')
			{
                rho_error = -rho_error;
			}
			if(USART1_BUF[5] != '+')
			{
				theta_error = -theta_error;
			}
            if(openmv_flag==11)
            {
                stop_5s_flag=1;
                stop_motor();
                ABS_motor(400,400);
                set_zhuanwan_output(0);
            }
            
			//PID运算
			servo_sum = SERVO_PD(&servo_pid);			
			float MOTOR = set_pwm - MOTOR_PI(&motor_pid);

			set_motor_output(MOTOR,MOTOR,MOTOR,MOTOR);
            set_zhuanwan_output(servo_sum);
        }
        
        if(mode_flag==1)
        {
            if(openmv_flag==10)
            if(stop_flag)
            {
                stop_motor();
            }
        }
        else if(mode_flag==2)
        {
            
        }
        else if(mode_flag==3)
        {
            
        }
        else if(mode_flag==4)
        {
            
        }
        else{ stop_motor();}
        if((exit_scanl==1||exit_scanr==1||mid_scan2_flag==1||mid_scan1_flag)&&stop_5s_flag==0&&stop_flag==0)
        {
            count++;
            if(count==20)
            {
                count=0;
                exit_scanl=0;
                exit_scanr=0;
                mid_scan1_flag=0;
                mid_scan2_flag=0;
                stop_5s_flag=0;
            }
            if(exit_scanl==1&&stop_5s_flag==0)
            {
                if(exit_scanr==1)
                {
                    count=0;
                    exit_scanl=0;
                    exit_scanr=0;
                     stop_5s_flag=1;
                    stop_motor();
                    ABS_motor(400,400);
                   set_zhuanwan_output(0);
                }
            }
            else if(exit_scanr==1&&stop_5s_flag==0)
            {
                if(exit_scanl==1)
                {
                    count=0;
                    exit_scanl=0;
                    exit_scanr=0;
                    stop_5s_flag=1;
                    stop_motor();
                    ABS_motor(400,400);
                    set_zhuanwan_output(0);
                }
            }
            

        }
				
		
}
void key_proce(void)
{
    if(click_M())
    {
        set_pwm+=100;
        
        if(set_pwm>750)
        {
            set_pwm=350;
           OLED_ShowNum(1,5,set_pwm,3);
        }
        else
        {
           OLED_ShowNum(1,5,set_pwm,3);

        }
        oled_display_speedlevel();
         
     }
    if(click_STAR())
     {
          //start_motor();
         mode_trans();
     }
    
}
void oled_display_speedlevel(void)
{
    switch((int)set_pwm)
    {
        case 350:
          OLED_ShowString(2,7,"0.3m/s");
            break;
        case 450:
          OLED_ShowString(2,7,"0.5m/s");
            break;
        case 550:
          OLED_ShowString(2,7,"0.7m/s");
            break;
        case 650:
          OLED_ShowString(2,7,"1.0m/s");
            break;
        case 750:
          OLED_ShowString(2,7,"1.2m/s");
            break;
        default:
            break;
        
    }
}
void mode_trans(void)
{
    switch(mode_flag)
    {
        case 0:
            mode_flag=1;
            start_motor();
            OLED_ShowString(3,7,"1");
            break;
        case 1:
            mode_flag=2;
            OLED_ShowString(3,7,"2");
            
            break;
        case 2:
            mode_flag=3;
            OLED_ShowString(3,7,"3");
            break;
        case 3:
            mode_flag=0;
            OLED_ShowString(3,7,"4");
            break;
        default:
            break;        
    }
}
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if(GPIO_Pin==L_scan_Pin)
    {
        if(HAL_GPIO_ReadPin(L_scan_GPIO_Port,L_scan_Pin)==1)
        {
            exit_scanl=1;  
            //set_zhuanwan_output(5);
        }
        __HAL_GPIO_EXTI_CLEAR_IT(L_scan_Pin);
    }
    if(GPIO_Pin==R_scan_Pin)
    {
        if(HAL_GPIO_ReadPin(R_scan_GPIO_Port,R_scan_Pin)==1)
        {
            exit_scanr=1;
            //set_zhuanwan_output(-5);
        }
        __HAL_GPIO_EXTI_CLEAR_IT(R_scan_Pin);
    }
    if(GPIO_Pin==mid_scan1_Pin)
    {
        if(HAL_GPIO_ReadPin(mid_scan1_GPIO_Port,mid_scan1_Pin)==1)
        {
            //mid_scan1_flag=1;
        }
        __HAL_GPIO_EXTI_CLEAR_IT(L_scan_Pin);
    }
    if(GPIO_Pin==mid_scan2_Pin)
    {
        if(HAL_GPIO_ReadPin(mid_scan2_GPIO_Port,mid_scan2_Pin)==1)
        {
            //mid_scan1_flag=1;
        }
        __HAL_GPIO_EXTI_CLEAR_IT(L_scan_Pin);
    }
    
    
}
