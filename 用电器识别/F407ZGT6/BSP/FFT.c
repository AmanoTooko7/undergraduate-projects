#include "FFT.h"
#include "usart.h"

unsigned char Tx_Buffer[8];
unsigned char RX_Buffer[40];
unsigned char read_enable,receive_finished,reveive_number;
unsigned long Voltage_data,Current_data,Power_data,Energy_data,Pf_data,CO2_data;

uint8_t USART2_RX_BUF[USART2_MAX_RECV_LEN];
uint8_t USART2_TX_BUF[USART2_MAX_SEND_LEN];
uint16_t USART2_RX_STA = 0;
uint8_t Rx2_buf=0;


uint8_t Rx_str[RX_MAX];
uint16_t Rx_point=0;
uint8_t Rx_buf=0;

unsigned int calccrc(unsigned char crcbuf,unsigned int crc)
{
    unsigned char i;
    unsigned char chk;
    crc=crc ^ crcbuf;
    for(i=0;i<8;i++)
    {
        chk=(unsigned char)(crc&1);
        crc=crc>>1;
        crc=crc&0x7fff;
        if (chk==1)
            crc=crc^0xa001;
        crc=crc&0xffff;
    }
    return crc;
}

unsigned int chkcrc(unsigned char *buf,unsigned char len)
{
    unsigned char hi,lo;
    unsigned int i;
    unsigned int crc;
    crc=0xFFFF;
    for(i=0;i<len;i++)
    {
        crc=calccrc(*buf,crc);
        buf++;
    }
    hi=( unsigned char)(crc%256);
    lo=( unsigned char)(crc/256);
    crc=(((unsigned int)(hi))<<8)|lo;
    return crc;
}
void read_data(void)
{
    union crcdata
    {
        unsigned int word16;
        unsigned char byte[2];
    }crcnow;
    
    if(read_enable==1) // 到时间抄读模块，抄读间隔1秒钟(或其他)
    {
        read_enable=0;
        Tx_Buffer[0]=Read_ID; //模块的ID号，默认ID为0x01
        Tx_Buffer[1]=0x03;
        Tx_Buffer[2]=0x00;
        Tx_Buffer[3]=0x48;
        Tx_Buffer[4]=0x00;
        Tx_Buffer[5]=0x08;
        crcnow.word16=chkcrc(Tx_Buffer,6);
        Tx_Buffer[6]=crcnow.byte[1]; //CRC效验低字节在前
        Tx_Buffer[7]=crcnow.byte[0];
        //发送8个数据，请根据单片机类型自己编程
        HAL_UART_Transmit(&huart2,Tx_Buffer,8,50);
        //printf("0x%x 0x%x 0x%x 0x%x 0x%x 0x%x 0x%x 0x%x\n",Tx_Buffer[0],Tx_Buffer[1],Tx_Buffer[2],Tx_Buffer[3],Tx_Buffer[4],Tx_Buffer[5],Tx_Buffer[6],Tx_Buffer[7]);
    }
}

bool Analysis_data(float *vol,float *cur,float *pow,float *pf,float *fre)
{
    union crcdata
    {
        unsigned int word16;
        unsigned char byte[2];
    }crcnow;
    
    read_data();
    //HAL_Delay(2000);
    if(receive_finished==1) //接收完成
    {
        receive_finished=0;
        reveive_number=USART2_RX_STA;
        USART2_RX_STA=0;
        if(RX_Buffer[0]==Read_ID||RX_Buffer[0] == 0x00) //确认ID正确
        {
            //printf("ok\n");
            crcnow.word16=chkcrc(RX_Buffer,reveive_number-2); //reveive_numbe是接收数据总长度
            if((crcnow.byte[0]==RX_Buffer[reveive_number-1])&&(crcnow.byte[1]==RX_Buffer[reveive_number-2]))
            {
                *vol=(float)((((unsigned long)(RX_Buffer[3]))<<24)|(((unsigned long)(RX_Buffer[4]))<<16)|(((unsigned long)(RX_Buffer[5]))<<8)|RX_Buffer[6])/10000;
                *cur=(float)((((unsigned long)(RX_Buffer[7]))<<24)|(((unsigned long)(RX_Buffer[8]))<<16)|(((unsigned long)(RX_Buffer[9]))<<8)|RX_Buffer[10])/1000;
                *pow=(float)((((unsigned long)(RX_Buffer[11]))<<24)|(((unsigned long)(RX_Buffer[12]))<<16)|(((unsigned long)(RX_Buffer[13]))<<8)|RX_Buffer[14])/10000;
                Energy_data=(((unsigned long)(RX_Buffer[15]))<<24)|(((unsigned long)(RX_Buffer[16]))<<16)|(((unsigned long)(RX_Buffer[17]))<<8)|RX_Buffer[18];
                *pf=(float)((((unsigned long)(RX_Buffer[19]))<<24)|(((unsigned long)(RX_Buffer[20]))<<16)|(((unsigned long)(RX_Buffer[21]))<<8)|RX_Buffer[22])/1000;
                CO2_data=(((unsigned long)(RX_Buffer[23]))<<24)|(((unsigned long)(RX_Buffer[24]))<<16)|(((unsigned long)(RX_Buffer[25]))<<8)|RX_Buffer[26];
                *fre=(float)((((unsigned long)(RX_Buffer[31])) << 24) | (((unsigned long)(RX_Buffer[32])) << 16) | (((unsigned long)(RX_Buffer[33]))<<8)| RX_Buffer[34])/100;
                
                return 1;
            }   
            return 0;            
        }
        else
        {
            return 0;
        }
    }
    return 0;
}
int fputc(int ch, FILE *f)
{
    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
    return ch;
}
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if(huart->Instance==USART1)
    {
        Rx_str[Rx_point++]=Rx_buf;
        HAL_UART_Receive_IT(huart,&Rx_buf,1);
    }
    else if(huart->Instance==USART2)
    {
        RX_Buffer[USART2_RX_STA++]=Rx2_buf;
        HAL_UART_Receive_IT(huart,&Rx2_buf,1);
    }    
}


void Uart1_Receive_Proc(void (*fun)(void))
{
    static bool Rx_flag=0;
    if(Rx_point!=0&&Rx_flag==0)
    {
        int cnt=Rx_point;
        HAL_Delay(1);
        if(cnt==Rx_point)
        {
            Rx_flag=1;
        }       
    }
    if(Rx_flag)
    {
        if(Rx_point==RX_Bit)
        {
            //printf("received:%s\n",Rx_str);
            (*fun)();
        }
        else
            //printf("receive error\n");
        Rx_flag=0;
        Rx_point=0;
    }
}
void Uart2_Receive_Proc(void)
{
    static bool Rx_flag=0;
    if(USART2_RX_STA!=0&&Rx_flag==0)
    {
        int cnt=USART2_RX_STA;
        HAL_Delay(1);
        if(cnt==USART2_RX_STA)
        {
            Rx_flag=1;
        }       
    }
    if(Rx_flag)
    {
        if(USART2_RX_STA==RX2_Bit)
        {
            receive_finished=1;
           // printf("uart2 ok\n");
        }
        else
        {
            //printf("uart2 error bit:%d\n",USART2_RX_STA);
        }
        Rx_flag=0;
        //USART2_RX_STA=0;
    }
}

