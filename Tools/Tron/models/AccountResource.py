#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：AccountResource.py
@Author  ：MoJeffrey
@Date    ：2023/5/11 16:47 
"""
class AccountResource:
    # int64 已使用的免费带宽
    freeNetUsed: int = 0

    # int64 免费带宽总量
    freeNetLimit: int = 0

    # int64 已使用的通过质押获得的带宽
    NetUsed: int = 0

    # int64 质押获得的带宽总量
    NetLimit: int = 0

    # int64 全网通过质押获取的带宽总量
    TotalNetLimit: int = 0

    # int64 全网用于获取带宽的质押TRX总量
    TotalNetWeight: int = 0

    # int64 全网获得的投票权总量
    totalTronPowerWeight: int = 0

    # int64 拥有的投票权
    tronPowerLimit: int = 0

    # int64 已使用的投票权
    tronPowerUsed: int = 0

    # int64 已使用的能量
    EnergyUsed: int = 0

    # int64 质押获取的总能量
    EnergyLimit: int = 0

    # int64 全网通过质押获取的能量总量
    TotalEnergyLimit: int = 0

    # int64 全网用于获取能量的质押TRX总量
    TotalEnergyWeight: int = 0

    # map<string, int64> 账户已使用的各个TRC10资产的免费带宽数量
    assetNetUsed = {}

    # map<string, int64> 账户中各个TRC10资产的免费带宽数量
    assetNetLimit = {}

    def __init__(self, Object: dict = None):
        if Object is not None:
            self.__dict__ = Object.copy()


    def GetCanUseEnergy(self) -> int:
        return self.EnergyLimit - self.EnergyUsed

    def GetCanUseBandWidth(self) -> int:
        return self.freeNetLimit - self.freeNetUsed + self.NetLimit - self.NetUsed
