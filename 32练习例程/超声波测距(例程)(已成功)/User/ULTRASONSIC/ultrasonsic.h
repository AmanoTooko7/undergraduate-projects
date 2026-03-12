#ifndef __ULTRASONSIC_H
#define __ULTRASONSIC_H

/*GPIOB*/
#define RCC_GPIOx RCC_APB2Periph_GPIOB
#define GPIOB_ULTR_PORT GPIOB
#define GPIOB_ULTR_Tx_PIN  GPIO_Pin_6
#define GPIOB_ULTR_Rx_PIN  GPIO_Pin_7

/*TIM2*/
#define BASIC_TIM          TIM2
#define BASIC_TIM_CLK				RCC_APB1Periph_TIM2
#define BASIC_TIM_IRQ 			TIM2_IRQn
#define BASIC_TIM_Period   	(1000-1)
#define BASIC_TIM_Prescaler (72-1)



void initHcsr04(void);
float Hcsr04GetLength(void );
#endif
