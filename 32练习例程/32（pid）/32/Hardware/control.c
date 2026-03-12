#include "control.h"

extern __IO int16_t EncoderOverflowCnt;
extern __IO int16_t EncoderOverflowCnt2;
__IO int encoderNow = 0;    /*当前时刻总计数值*/
int temp=0;

//周期定时器的回调函数
void AutoReloadCallback()   //0.01s
{
   static uint32_t location_timer = 0;    // 位置环周期
    
	 
    static __IO int encoderLast = 0;   /*上一时刻总计数值*/
	int encoderDelta = 0; /*当前时刻与上一时刻编码器的变化量*/
    
    float actual_speed = 0;  /*实际测得速度*/
	int actual_speed_int = 0;
	
	int res_pwm = 0;/*PID计算得到的PWM值*/
	static int i=0;
	
	/*【1】读取编码器的值*/
	encoderNow =( read_encoder() + EncoderOverflowCnt*ENCODER_TIM_PERIOD);/*获取当前的累计值*/
	encoderDelta = encoderNow - encoderLast; /*得到变化值*/
	encoderLast = encoderNow;/*更新上次的累计值*/
 
	/*【2】PID运算，得到PWM控制值*/
//    res_pwm = pwm_val_protect((int)PID_realize(encoderDelta));/*传入编码器的[变化值]，实现电机【速度】控制*/
//	//res_pwm = pwm_val_protect((int)PID_realize(encoderNow));/*传入编码器的[总计数值]，实现电机【位置】控制*/
    	/*【2】位置PID运算，得到PWM控制值*/
	if ((location_timer++ % 2) == 0)
	{
		float control_val = 0;   /*当前控制值*/
		
		/*位置PID计算*/
		control_val = location_pid_realize(&pid_location, encoderNow);  
		
        /*目标速度值限制*/
		speed_val_protect(&control_val);

		/*设定速度PID的目标值*/
		set_pid_target(&pid_speed, control_val);    

		#if defined(PID_ASSISTANT_EN)
		if ((location_timer % 16) == 8)
		{
			temp = (int)control_val;
			set_computer_value(SEND_TARGET_CMD, CURVES_CH2, &temp, 1);     // 给通道 2 发送目标值
		}
		#endif
	}	  
	/* 转速(1秒钟转多少圈)=单位时间内的计数值/总分辨率*时间系数, 再乘60变为1分钟转多少圈 */
    actual_speed = (float)encoderDelta / TOTAL_RESOLUTION * 10*60;
    
	/*【3】速度PID运算，得到PWM控制值*/
	//actual_speed_int = actual_speed;
	res_pwm = pwm_val_protect((int)speed_pid_realize(&pid_speed, actual_speed));
    
	/*【3】PWM控制电机*/
	set_motor_output(res_pwm,res_pwm);
	
	/*【4】数据上传到上位机显示*/
#if (PID_ASSISTANT_EN)
	i++;
	if(i%12 == 5) //(i==12)
	{
        set_computer_value(SEND_FACT_CMD, CURVES_CH1, &encoderNow, 1);   /*给通道1发送实际的电机【位置】值*/
         printf("SPEED：%d. PLACE：%d, TARGETPLACE：%.0f\n", actual_speed, encoderNow, get_pid_target(&pid_location)); 
    }
#else
	i++;
	if(i==100)
	{
		i=0;
		//printf("sum:%d set_pwm:%d\r\n",0,res_pwm);
        printf("实际值速度：%d. 实际位置值：%d, 目标位置值：%.0f\n", actual_speed, encoderNow, get_pid_target(&pid_location)); 

		
	}
#endif
}

int pwm_val_protect(int pwm_input)
{
	int pwm_output = 0;
	
	if(pwm_input>999) 
	{
		pwm_output = 999;
	}
	else if(pwm_input<-999) 
	{
		pwm_output = -999;
	}
	else if((pwm_input>-50)&&(pwm_input<50)) 
	{
		pwm_output = 0;
	}
	else
	{
		pwm_output = pwm_input;
	}
	
	return pwm_output;
}
//目标速度值限制
//#define TARGET_SPEED_MAX   60 // 目标速度的最大值 r/m
static float TARGET_SPEED_MAX = 60.0;

static void speed_val_protect(float *speed_val)
{
	/*目标速度上限处理*/
	if (*speed_val > TARGET_SPEED_MAX)
	{
		*speed_val = TARGET_SPEED_MAX;
	}
	else if (*speed_val < -TARGET_SPEED_MAX)
	{
		*speed_val = -TARGET_SPEED_MAX;
	}	
}

/*上位机目标值获取与设置*/
void SetTargetMaxSpeed(int speed)
{
	TARGET_SPEED_MAX = (float)speed;
}
int GetTargetMaxSpeed(void)
{
	return (int)TARGET_SPEED_MAX;
}