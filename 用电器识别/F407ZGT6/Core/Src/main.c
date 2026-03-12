/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "dac.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "FFT.h"
#include "Appliances.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
extern uint32_t sys_tick;

uint8_t LCD_Task=0;
uint8_t Measure_Task=0;
uint8_t Scan_Remote_Task=0;
uint8_t bl_task=0;
uint16_t Task_cnt=0;
 

uint32_t I_temp,T_temp,V_temp,P_temp,PF_temp;
uint8_t Status;
uint8_t learn_flag=0x00;	//自学习标志位,通过按键切换
uint8_t app_num=0;
uint8_t learn_flag_0 = 0;
uint8_t measure_flag=0;
uint8_t menu_flag=1;

uint32_t ccr1_val,ccr2_val,Frq_val;
float Duty_val;

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    if(htim->Instance==TIM3)
    {
        ccr2_val=HAL_TIM_ReadCapturedValue(htim,TIM_CHANNEL_1);
        ccr1_val=HAL_TIM_ReadCapturedValue(htim,TIM_CHANNEL_2);
        __HAL_TIM_SetCounter(htim,0);
        Frq_val=(80000000/80/ccr2_val);
        Duty_val=((float)ccr1_val/(float)ccr2_val)*100;
        if(Frq_val>10000)
        {
            Frq_val=0;Duty_val=0;
        }
        if(Duty_val>100)
            Duty_val=0;
        HAL_TIM_IC_Start(htim,TIM_CHANNEL_1);
        HAL_TIM_IC_Start(htim,TIM_CHANNEL_2);
    }
}

void learn_mode(void)
{
	char tbuf[32];
	float voltage;			//测量电压
	float Current;			//测量电流
	float Pow_fac;			//功率因数
	float Pactive_pow;	//有功功率
	float frequency;
    int i=0;

	
    if(learn_flag_0==1)
    {
        learn_flag_0=0;
        if(Analysis_data(&Current_proper.voltage,&Current_proper.Current,&Current_proper.Pactive_pow,&Current_proper.Pow_fac,&Current_proper.frequency)==1)
        {
            if(app_num==1)
            {
                app1.Current			=Current_proper.Current;
                app1.voltage			=Current_proper.voltage;
                app1.Pactive_pow	=Current_proper.Pactive_pow;
                app1.Pow_fac			=Current_proper.Pow_fac;
            }
            else if(app_num==2)
            {
                app2.Current			=Current_proper.Current;
                app2.voltage			=Current_proper.voltage;
                app2.Pactive_pow	=Current_proper.Pactive_pow;
                app2.Pow_fac			=Current_proper.Pow_fac;
            }
            else if(app_num==3)
            {
                app3.Current			=Current_proper.Current;
                app3.voltage			=Current_proper.voltage;
                app3.Pactive_pow	=Current_proper.Pactive_pow;
                app3.Pow_fac			=Current_proper.Pow_fac;
            }		
            else if(app_num==4)
            {
                app4.Current			=Current_proper.Current;
                app4.voltage			=Current_proper.voltage;
                app4.Pactive_pow	=Current_proper.Pactive_pow;
                app4.Pow_fac			=Current_proper.Pow_fac;
            }		
            else if(app_num==5)
            {
                app5.Current			=Current_proper.Current;
                app5.voltage			=Current_proper.voltage;
                app5.Pactive_pow	=Current_proper.Pactive_pow;
                app5.Pow_fac			=Current_proper.Pow_fac;
            }		
            else if(app_num==6)
            {
                app6.Current			=Current_proper.Current;
                app6.voltage			=Current_proper.voltage;
                app6.Pactive_pow	=Current_proper.Pactive_pow;
                app6.Pow_fac			=Current_proper.Pow_fac;
            }		
            else if(app_num==7)
            {
                app7.Current			=Current_proper.Current;
                app7.voltage			=Current_proper.voltage;
                app7.Pactive_pow	=Current_proper.Pactive_pow;
                app7.Pow_fac			=Current_proper.Pow_fac;
            }
            printf("gun_flag.val=1\xff\xff\xff");
            //
        }
    }
		
}

void JudgeSta(void)
{
	int ElectricalSta[7]={0};	//用电器工作状态	
	int len=7;
	int i=0,j=0;
	float p_sta[7];			
	float p_sum;			//总功率
	float current;
	
	float   power[7]={app1.Pactive_pow,app2.Pactive_pow,app3.Pactive_pow,app4.Pactive_pow,app5.Pactive_pow,app6.Pactive_pow,app7.Pactive_pow};
	int times=0,timestmp=0;
    
    
	for( i=0;i<7;i++)
	{
			switch(i)
			{
				case 0:app1.sta="off"; printf("sw0.val=0\xff\xff\xff");break;
				case 1:app2.sta="off"; printf("sw1.val=0\xff\xff\xff");break;
				case 2:app3.sta="off"; printf("sw2.val=0\xff\xff\xff");break;
				case 3:app4.sta="off"; printf("sw3.val=0\xff\xff\xff");break;
				case 4:app5.sta="off"; printf("sw4.val=0\xff\xff\xff");break;
				case 5:app6.sta="off"; printf("sw5.val=0\xff\xff\xff");break;
				case 6:app7.sta="off"; printf("sw6.val=0\xff\xff\xff");break;
	 		}
	}
	for(times=0;times<128;times++)
	{
		timestmp=times;
		for(i=0;i<7;i++) 
		ElectricalSta[i]=0; 
		i=0;
		while(timestmp)
		{
			ElectricalSta[i]=timestmp%2;
			timestmp=timestmp/2;
			i++;
		}
		for(i = 0; i < len; i ++)//遍历数组。
		{
			p_sta[i] = ElectricalSta[i]*power[i];
		}
		for(i=0;i<7;i++) 
		{
			p_sum+=p_sta[i];
		}
		if(p_sum<60)
        {
            if(fabsf(p_sum-Current_proper.Pactive_pow)<0.8)  //进行匹配 假设匹配PowerSum
            {
                for( i=0;i<7;i++)
                {
                    if(ElectricalSta[i]==1)
                    {
                        switch(i)
                        {
                            case 0:app1.sta="on"; printf("sw0.val=1\xff\xff\xff");break;
                            case 1:app2.sta="on"; printf("sw1.val=1\xff\xff\xff");break;
                            case 2:app3.sta="on"; printf("sw2.val=1\xff\xff\xff");break;
                            case 3:app4.sta="on"; printf("sw3.val=1\xff\xff\xff");break;
                            case 4:app5.sta="on"; printf("sw4.val=1\xff\xff\xff");break;
                            case 5:app6.sta="on"; printf("sw5.val=1\xff\xff\xff");break;
                            case 6:app7.sta="on"; printf("sw6.val=1\xff\xff\xff");break;
                        }
                    }
                }
                p_sum=0;
                break;
            }
            p_sum=0;
        }
		else
		{
            if(fabsf(p_sum-Current_proper.Pactive_pow)<1.5)  //进行匹配 假设匹配PowerSum
            {
                for( i=0;i<7;i++)
                {
                    if(ElectricalSta[i]==1)
                    {
                        switch(i)
                        {
                            case 0:app1.sta="on"; printf("sw0.val=1\xff\xff\xff");break;
                            case 1:app2.sta="on"; printf("sw1.val=1\xff\xff\xff");break;
                            case 2:app3.sta="on"; printf("sw2.val=1\xff\xff\xff");break;
                            case 3:app4.sta="on"; printf("sw3.val=1\xff\xff\xff");break;
                            case 4:app5.sta="on"; printf("sw4.val=1\xff\xff\xff");break;
                            case 5:app6.sta="on"; printf("sw5.val=1\xff\xff\xff");break;
                            case 6:app7.sta="on"; printf("sw6.val=1\xff\xff\xff");break;
                        }
                    }
                }
                p_sum=0;
                break;
            }
            p_sum=0;
		}
	}
	
}
void Main_Proc(void)
{
    char buf[20];
    static uint8_t sta=0;
    if(bl_task==1)
    {
        bl_task=0;
        read_enable=1;
        Analysis_data(&Current_proper.voltage,&Current_proper.Current,&Current_proper.Pactive_pow,&Current_proper.Pow_fac,&Current_proper.frequency);
        printf("t14.txt=\"频率:%.2fHz\"\xff\xff\xff",Current_proper.frequency);
        printf("t10.txt=\"电压:%.2fV\"\xff\xff\xff",Current_proper.voltage);
        printf("t12.txt=\"总功率:%.2fW\"\xff\xff\xff",Current_proper.Pactive_pow);
        printf("t13.txt=\"功率因数:%.2f\"\xff\xff\xff",Current_proper.Pow_fac);  
        printf("t11.txt=\"电流:%.2fA\"\xff\xff\xff",Current_proper.Current);
        switch(sta)
        {
            case 0:
                sprintf(buf,"vol:%3.2f\r\n",Current_proper.voltage);
                HAL_UART_Transmit(&huart3,(const uint8_t*)buf,strlen(buf),50);  
                sta=1;
                break;
            case 1:
                sprintf(buf,"cur:%3.2f\r\n",Current_proper.Current);
                HAL_UART_Transmit(&huart3,(const uint8_t*)buf,strlen(buf),50);
                sta=2;
                break;
            case 2:
                sprintf(buf,"pow:%3.2f\r\n",Current_proper.Pactive_pow);
                HAL_UART_Transmit(&huart3,(const uint8_t*)buf,strlen(buf),50);
                sta=3;
                break;
            case 3:
                sprintf(buf,"frq:%3.2f\r\n",Current_proper.frequency);
                HAL_UART_Transmit(&huart3,(const uint8_t*)buf,strlen(buf),50);
                sta=4;
                break;
            case 4:
                sprintf(buf,"pf:%3.2f\r\n",Current_proper.Pow_fac);
                HAL_UART_Transmit(&huart3,(const uint8_t*)buf,strlen(buf),50);
                sta=0;
                break;
        }
    }
    if(measure_flag==1)
    {
        if(Measure_Task == 1)
        {
            Measure_Task=0;
            JudgeSta();
        }
    }
    else if(learn_flag==1)
    {
        learn_mode();
    }
    
/*    if(Scan_Remote_Task==1)
    {
        Scan_Remote_Task=0;
        //key1 = Remote_Scan();						//扫描红外遥控信号并接收
    
        if(menu_flag==1)
        {
            switch(key1){
                case 162:				//CH-
                    learn_flag=1;
                    menu_flag=0;
                    //LCD_Clear(WHITE);
                break;					//切换学习模式
                case 226:				//CH+
                    measure_flag=1;
                    menu_flag=0;
                    //LCD_Clear(WHITE);
                break;//切换
            }
        }
        if(learn_flag == 1)
        {
            switch(key1)
            {
                //选择自学习用电器编号
                case 48		:	
                    learn_flag_0=1;
                    app_num =1;
                break;
                    case 24		:
                        learn_flag_0=1;
                        app_num =2;
                break;
                    case 122	:	
                        learn_flag_0=1;
                        app_num =3;
                break;
                  case 16		:	
                      learn_flag_0=1;
                      app_num =4;
                break;
                  case 56		:	
                      learn_flag_0=1;
                      app_num =5;
                break;
                case 90		:
                    learn_flag_0=1;
                    app_num =6;
                break;
                case 66		:	
                    learn_flag_0=1;
                    app_num =7;
                break;
                case 98		:				//退出键
                    app_num=0;
                    learn_flag=0;
                    learn_flag_0=0;
                    menu_flag=1;
                    //LCD_Clear(WHITE);
                    //LCD_Display_Handle();
                break;
            }
        
        }
        if(measure_flag == 1)
        {
            switch(key1)
            {
                case 98	:
                    measure_flag=0;
                    menu_flag=1;
                    //LCD_Clear(WHITE);
                    //LCD_Display_Handle();
                    break;
            }
        }
    }
    */
}
void Uart1_Proc(void)
{
    int i=0;
    if(Rx_str[0]==0x01)
    {
        if(Rx_str[1]==0x02)
        {
            for( i=0;i<7;i++)
            {
                switch(i)
                {
                    case 0:app1.sta="off"; printf("sw0.val=0\xff\xff\xff");break;
                    case 1:app2.sta="off"; printf("sw1.val=0\xff\xff\xff");break;
                    case 2:app3.sta="off"; printf("sw2.val=0\xff\xff\xff");break;
                    case 3:app4.sta="off"; printf("sw3.val=0\xff\xff\xff");break;
                    case 4:app5.sta="off"; printf("sw4.val=0\xff\xff\xff");break;
                    case 5:app6.sta="off"; printf("sw5.val=0\xff\xff\xff");break;
                    case 6:app7.sta="off"; printf("sw6.val=0\xff\xff\xff");break;
                }
            }
            if(Rx_str[2]==0)
            {
                learn_flag_0=0;
                learn_flag=0;
                measure_flag=1;
            }
            else if(Rx_str[2]==1)
            {
                learn_flag=1;
                measure_flag=0;
            }
        }
        else if(Rx_str[1]==0x03)
        {
            switch(Rx_str[2])
            {
                case 1:app_num=1;
                learn_flag_0=1;
                    break;
                case 2:app_num=2;
                learn_flag_0=1;
                    break;
                case 3:app_num=3;
                learn_flag_0=1;
                    break;
                case 4:app_num=4;
                learn_flag_0=1;
                    break;
                case 5:app_num=5;
                learn_flag_0=1;
                    break;
                case 6:app_num=6;
                learn_flag_0=1;
                    break;
                case 7:app_num=7;
                learn_flag_0=1;
                    break;     
                default:break;
            }
        }
    }

}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DAC_Init();
  MX_TIM3_Init();
  MX_TIM4_Init();
  MX_TIM6_Init();
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  MX_USART3_UART_Init();
  /* USER CODE BEGIN 2 */
    HAL_UART_Receive_IT(&huart1,&Rx_buf,1);
    HAL_UART_Receive_IT(&huart2,&Rx2_buf,1);
    HAL_TIM_PWM_Start(&htim4,TIM_CHANNEL_1);
    HAL_TIM_IC_Start_IT(&htim3,TIM_CHANNEL_1);
    //printf("hello\n");
    HAL_Delay(1000);
    measure_flag=1;
    printf("g1.txt=\"正在联网中...\"\xff\xff\xff");
    HAL_Delay(3000);
    printf("g1.txt=\"已连接互联网平台..\"\xff\xff\xff");
    //read_enable=1;
    //read_data();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
      Uart2_Receive_Proc();
      Uart1_Receive_Proc(Uart1_Proc);
      Main_Proc();
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 15;
  RCC_OscInitStruct.PLL.PLLN = 96;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
