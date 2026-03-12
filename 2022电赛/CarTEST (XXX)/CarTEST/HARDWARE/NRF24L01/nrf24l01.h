#ifndef __NRF24L01_H_
#define __NRF24L01_H_

#include "main.h"
#include "spi.h"
#include <stdio.h>
#include <string.h>

#define SPI1_CE(x)		HAL_GPIO_WritePin(GPIOB,GPIO_PIN_3,x)
#define SPI1_CS(x)		HAL_GPIO_WritePin(GPIOB,GPIO_PIN_4,x)

#define SPI2_CE(x)		HAL_GPIO_WritePin(GPIOB,GPIO_PIN_3,x)
#define SPI2_CS(x)		HAL_GPIO_WritePin(GPIOB,GPIO_PIN_4,x)

#define IRQ_READ()      HAL_GPIO_ReadPin(GPIOB,GPIO_PIN_7)

#define NRF_WRITE_REG 0x20
typedef struct
{
	uint8_t cmd;
	uint8_t data[7];
	uint8_t len;
}data_t;

extern uint8_t rxbuff[32];		

void NRF24L01_TX_Mode(SPI_HandleTypeDef *spi);
void NRF24L01_RX_Mode(SPI_HandleTypeDef *spi);

uint8_t NRF24L01_TxPacket(SPI_HandleTypeDef *spi,uint8_t *txbuf);
uint8_t NRF24L01_RxPacket(SPI_HandleTypeDef *spi,uint8_t *rxbuf);

//void nrf24l01_test();
#endif /* __NRF24L01_H_ */

