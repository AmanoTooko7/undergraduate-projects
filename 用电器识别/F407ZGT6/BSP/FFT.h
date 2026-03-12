#ifndef _FFT_H
#define _FFT_H
#include "main.h"
#include "tim.h"

#define RX_MAX 50
#define RX_Bit 3

#define RX2_Bit 37  //29
#define USART2_MAX_RECV_LEN		300					//最大接收缓存字节数
#define USART2_MAX_SEND_LEN		300					//最大发送缓存字节数
#define Read_ID 0x01

extern unsigned char Tx_Buffer[8];
extern unsigned char RX_Buffer[40];
extern unsigned char read_enable,receive_finished,reveive_number;
extern unsigned long Voltage_data,Current_data,Power_data,Energy_data,Pf_data,CO2_data;


extern uint8_t Rx_str[RX_MAX];
extern uint16_t Rx_point;
extern uint8_t Rx_buf;

extern uint8_t Rx2_buf;
extern uint8_t USART2_RX_BUF[USART2_MAX_RECV_LEN];
extern uint8_t USART2_TX_BUF[USART2_MAX_SEND_LEN];
extern uint16_t USART2_RX_STA;




bool Analysis_data(float *vol,float *cur,float *pow,float *pf,float *fre);
void Uart1_Receive_Proc(void (*fun)(void));
void Uart2_Receive_Proc(void);
void read_data(void);

#endif
