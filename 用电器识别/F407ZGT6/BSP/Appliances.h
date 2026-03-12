#ifndef _APP_H
#define _APP_H


typedef struct mea_proper{
	float voltage;			//测量电压
	float Current;			//测量电流
	float Pow_fac;			//功率因数
	float Pactive_pow;	//有功功率
	float frequency;		//电网频率
}mea_proper;

typedef struct ele_app{
	float voltage;			//测量电压
	float Current;			//测量电流
	float Pow_fac;			//功率因数
	float Pactive_pow;	//有功功率
	char	*sta;
}ele_app;


extern mea_proper Current_proper;
extern ele_app app1;
extern ele_app app2;
extern ele_app app3;
extern ele_app app4;
extern ele_app app5;
extern ele_app app6;
extern ele_app app7;

#endif