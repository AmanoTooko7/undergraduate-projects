#include "nrf24l01.h"

#define NRF_TX
#define NRF_RX
        
uint8_t rxbuff[32];				


uint8_t SPIx_ReadWriteByte(SPI_HandleTypeDef* hspi,uint8_t byte)
{
  uint8_t d_read,d_send=byte;
  if(HAL_SPI_TransmitReceive(hspi,&d_send,&d_read,1,0xFF)!=HAL_OK)
  {
    d_read=0xFF;
  }
  return d_read; 
}

uint8_t NRF24L01_Write_Reg(SPI_HandleTypeDef * spi,uint8_t reg,uint8_t value)
{
	uint8_t status;	
    if(spi->Instance == SPI1)//使能SPI传输
    {
		SPI1_CS(0);
	}
	else
	{
		SPI2_CS(0);
	}
  status =SPIx_ReadWriteByte(spi,reg);   //发送寄存器号 
  SPIx_ReadWriteByte(spi,value);         //写入寄存器的值
    if(spi->Instance == SPI1) //禁止SPI传输
    {
		SPI1_CS(1);
	}
	else
	{
		SPI2_CS(1);
	}               	   
  return(status);       			//返回状态值
}


uint8_t NRF24L01_Read_Reg(SPI_HandleTypeDef * spi,uint8_t reg)
{
	uint8_t reg_val;	    
    if(spi->Instance == SPI1)//使能SPI传输
    {
		SPI1_CS(0);
	}
	else
	{
		SPI2_CS(0);
	}
  SPIx_ReadWriteByte(spi,reg);   //发送寄存器号
  reg_val=SPIx_ReadWriteByte(spi,0XFF);//读取寄存器内容
    if(spi->Instance == SPI1) //禁止SPI传输
    {
	SPI1_CS(1);
	}
	else
	{
		SPI2_CS(1);
	}	    
  return(reg_val);           //返回状态值
}

uint8_t NRF24L01_Read_Buf(SPI_HandleTypeDef * spi,uint8_t reg,uint8_t *pBuf,uint8_t len)
{
	uint8_t status,uint8_t_ctr;	   
  
   if(spi->Instance == SPI1)//使能SPI传输
  {
	SPI1_CS(0);
	}
	else
	{
		SPI2_CS(0);
	}
  status=SPIx_ReadWriteByte(spi,reg);//发送寄存器值(位置),并读取状态值   	   
 	for(uint8_t_ctr=0;uint8_t_ctr<len;uint8_t_ctr++)
  {
    pBuf[uint8_t_ctr]=SPIx_ReadWriteByte(spi,0XFF);//读出数据
  }
    if(spi->Instance == SPI1) //禁止SPI传输
  {
	SPI1_CS(1);
	}
	else
	{
		SPI2_CS(1);
	}
  return status;        //返回读到的状态值
}

uint8_t NRF24L01_Write_Buf(SPI_HandleTypeDef * spi,uint8_t reg, uint8_t *pBuf, uint8_t len)
{
	uint8_t status,uint8_t_ctr;	    
    if(spi->Instance == SPI1)//使能SPI传输
  {
	SPI1_CS(0);
	}
	else
	{
		SPI2_CS(0);
	}
  status = SPIx_ReadWriteByte(spi,reg);//发送寄存器值(位置),并读取状态值
  for(uint8_t_ctr=0; uint8_t_ctr<len; uint8_t_ctr++)
  {
    SPIx_ReadWriteByte(spi,*pBuf++); //写入数据	 
  }
    if(spi->Instance == SPI1) //禁止SPI传输
  {
	SPI1_CS(1);
	}
	else
	{
		SPI2_CS(1);
	}
  return status;          //返回读到的状态值
}


uint8_t NRF24L01_RxPacket(SPI_HandleTypeDef *spi,uint8_t *rxbuf)
{
	uint8_t sta;

	sta=NRF24L01_Read_Reg(spi,0x07);  //读取状态寄存器的值    	 
	NRF24L01_Write_Reg(spi,0x20+0x07,sta); //清除RX_DR中断标志
	if(sta&0x40)//接收到数据
	{
		NRF24L01_Read_Buf(spi,0x61,rxbuf,32);//读取数据
		NRF24L01_Write_Reg(spi,0xe2,0xff);//清除RX FIFO寄存器 
		return 0; 
	}	   
	return 1;//没收到任何数据
}

uint8_t NRF24L01_TxPacket(SPI_HandleTypeDef *spi,uint8_t *txbuf)
{
    uint8_t sta;
    SPI1_CE(0);
    NRF24L01_Write_Buf(spi,0xa0, txbuf, 32); //写数据到TX BUF  32个字节
    SPI1_CE(1);                                              //启动发送
	
	
	
	while(IRQ_READ() != 0){};
	
    sta = NRF24L01_Read_Reg(spi,0x07);                 //读取状态寄存器的值
    NRF24L01_Write_Reg(spi,0x20 + 0x07, sta);      //清除TX_DS或MAX_RT中断标志
    if (sta & 0x10)                                //达到最大重发次数
    {
        NRF24L01_Write_Reg(spi,0xe1, 0xff); //清除TX FIFO寄存器
        return 0x10;
    }
    if (sta & 0x20) //发送完成
    {
        return 0x20;
    }
    return 0xff; //其他原因发送失败
}
void NRF24L01_RX_Mode(SPI_HandleTypeDef *spi)
{
	uint8_t addr[5] = {0xa1,0xa2,0xa3,0xa4,0xa5};
    SPI2_CE(0);
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x00, 0x0F);    //配置基本工作模式的参数;PWR_UP,EN_CRC,16BIT_CRC
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x01, 0x01);     //使能通道0的自动应答
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x02, 0x01); //使能通道0的接收地址
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x05, 40);       //设置RF通信频率
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x06, 0x0f);  //设置TX发射参数,0db增益,2Mbps,低噪声增益开启

    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x11, 32); //选择通道0的有效数据宽度

    NRF24L01_Write_Buf(spi,NRF_WRITE_REG + 0x0a, addr, 5); //写RX节点地址

    SPI2_CE(1); // CE为高,进入接收模式
    HAL_Delay(1);
}


void NRF24L01_TX_Mode(SPI_HandleTypeDef *spi)
{
	uint8_t addr[5] = {0xa1,0xa2,0xa3,0xa4,0xa5};
    SPI1_CE(0);
    NRF24L01_Write_Buf(spi,NRF_WRITE_REG + 0x10, addr, 5);    //写TX节点地址
    NRF24L01_Write_Buf(spi,NRF_WRITE_REG + 0x0A, addr, 5); //设置TX节点地址,主要为了使能ACK

    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x01, 0x01);      //使能通道0的自动应答
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x02, 0x01);  //使能通道0的接收地址
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x04, 0x1a); //设置自动重发间隔时间:4000us + 86us;最大自动重发次数:15次
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x05, 40);        //设置RF通道为40
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x06, 0x0f);   //设置TX发射参数,0db增益,2Mbps,低噪声增益开启
    NRF24L01_Write_Reg(spi,NRF_WRITE_REG + 0x00, 0x0e);     //配置基本工作模式的参数;PWR_UP,EN_CRC,16BIT_CRC,接收模式,开启所有中断
    SPI1_CE(1);                                              // CE为高,10us后启动发送
    HAL_Delay(1);

}
void nrf24l01_test()
{
	SPI1_CE(0);
	NRF24L01_Write_Reg(&hspi1,NRF_WRITE_REG + 0x06, 0x0f);   //设置TX发射参数,0db增益,2Mbps,低噪声增益开启
	SPI1_CE(1);
	printf("0x06 value:%0x",NRF24L01_Read_Reg(&hspi1,0x06));	
}



