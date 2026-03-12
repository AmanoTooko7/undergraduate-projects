#include "stm32f10x.h"                  // Device header
 
 /*见PPT77
 1.开启rcc时钟(ADC的CLK和GPIO的时钟)
 2.配置GPIO为模拟输入模式
 3.配置多路开关，也就是选哪个GPIO口进入规则组列表
 4.配置ADC转换器(单次或连续转换,扫描或非扫描,有几个通道,触发源是什么,数据对其方式)
 5.可配置模拟看门狗，中断(本节不用)
 6.调用ADC_Cmd函数，开启ADC，就能正常工作了
 7.对ADC进行校准
 */
 void AD_Init(void){
	
	//第一步
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

	RCC_ADCCLKConfig(RCC_PCLK2_Div6);//对ADC进行时钟配置72MHz/6=12MHz
	 
	 //第二步初始化PA0为模拟输入
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;//模拟输入,这里的GPIO_Mode_AIN是ADC的专属模式
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure); 
	 //第三步，表示在规则组菜单一共16个序列里列表里选择第一个序列(第三个参数),写入通道0，第四个参数随便选
	ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_55Cycles5);
	 //第四步初始化ADC
	 ADC_InitTypeDef ADC_InitStruct;
	 ADC_InitStruct.ADC_Mode = ADC_Mode_Independent;//ADC独立模式
	 ADC_InitStruct.ADC_ScanConvMode = DISABLE;//选择扫描转换还是非扫描模式，为非扫描模式
	 ADC_InitStruct.ADC_ContinuousConvMode = DISABLE;//选择连续转换模式或单次转换模式，为单次扫描模式
											  //此对应PPT91页四种模式
	 ADC_InitStruct.ADC_NbrOfChannel = 1;//在扫描模式下总共会用到几个通道
	 ADC_InitStruct.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;//外部触发源转换选择，这里不用外部触发，是内部软件触发
	 ADC_InitStruct.ADC_DataAlign = ADC_DataAlign_Right;//数据对其模式，选右对齐
	 
	 ADC_Init(ADC1, &ADC_InitStruct);
	 
	 //第五步若需要中断和模拟看门狗就可在后面配置
	 
	 //第六步开启ADC电源
	 ADC_Cmd(ADC1, ENABLE);
	 //对ADC进行校准,完全看不懂
	 ADC_ResetCalibration(ADC1);
	 while (ADC_GetCalibrationStatus(ADC1) == SET);
	 ADC_StartCalibration(ADC1);
	 while (ADC_GetCalibrationStatus(ADC1) == SET);
 }
 
 uint16_t AD_GetValue(void){
	 
	 ADC_SoftwareStartConvCmd(ADC1, ENABLE);//软件触发转换
 	 while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET);//规则组转换完成标志位,==RESET，也就是等于0表示转化未完成
															//此时while为真，转换完成后则不等于RESET为假，跳出while循环
															//此句表示等待ADC转换完成
	 return ADC_GetConversionValue(ADC1);					//获取ADC转化的结果
	   
 }
 
 
 