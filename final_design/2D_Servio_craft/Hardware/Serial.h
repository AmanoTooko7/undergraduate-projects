#ifndef __SERIAL_H
#define __SERIAL_H

#include <stdio.h>

extern uint8_t Serial_RxFlag;

extern uint8_t rx_buffer[];
extern uint32_t x1, y1, x2, y2, x3, y3, x4, y4;
extern uint32_t a, b;

void Serial_Init(void);
void Serial_SendByte(uint8_t Byte);
void Serial_SendArray(uint8_t *Array, uint16_t Length);
void Serial_SendString(char *String);
void Serial_SendNumber(uint32_t Number, uint8_t Length);
void Serial_Printf(char *format, ...);

void Serial_SendPacket(void);
void parse_rect(uint8_t* rx_buffer);
void parse_laser(uint8_t* rx_buffer);
uint8_t Serial_GetRxFlag(void);

#endif
