#include "iwdg.h"

void init_iwdg(u8 prer,u16 rlr)
{
    IWDG_WriteAccessCmd(IWDG_WriteAccess_Enable);
    IWDG_SetPrescaler(prer);
    IWDG_SetReload(rlr);
    IWDG_ReloadCounter();
    IWDG_Enable();
}

void feed_iwdg()
{
    IWDG_ReloadCounter();
}
