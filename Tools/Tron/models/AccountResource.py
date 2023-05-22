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

    # 用于计算质押TRX = 多少能量
    __TotalEnergyLimit: int = None
    __TotalEnergyWeight: int = None

    # 用于计算质押TRX = 多少宽带
    __TotalNetLimit: int = None
    __TotalNetWeight: int = None

    # 用于计算FeeLimit
    __BandWidthPrices: int = None
    __EnergyPrices: int = None

    def __init__(self, Object: dict = None):
        if Object is not None:
            self.__dict__ = Object.copy()
            AccountResource.__TotalEnergyLimit = self.TotalEnergyLimit
            AccountResource.__TotalEnergyWeight = self.TotalEnergyWeight

    def GetCanUseEnergy(self) -> int:
        return self.EnergyLimit - self.EnergyUsed

    def GetCanUseBandWidth(self) -> int:
        return self.freeNetLimit - self.freeNetUsed + self.NetLimit - self.NetUsed

    @staticmethod
    def SetBandWidthPrices(BandWidthPrices: int):
        AccountResource.__BandWidthPrices = BandWidthPrices

    @staticmethod
    def SetEnergyPrices(EnergyPrices: int):
        AccountResource.__EnergyPrices = EnergyPrices

    @staticmethod
    def GetFeeLimit(BandWidth: int, EnergyRequired: int) -> int:
        if AccountResource.__BandWidthPrices is None:
            raise Exception("未获取宽带单价")

        if AccountResource.__EnergyPrices is None:
            raise Exception("未获取能量单价")

        return int(BandWidth * AccountResource.__BandWidthPrices + AccountResource.__EnergyPrices * EnergyRequired)

    @staticmethod
    def GetSumForEnergy(Energy: float) -> int:
        if AccountResource.__TotalEnergyLimit is None:
            raise Exception("未获取全网质押TRX")

        return int(1 / AccountResource.__TotalEnergyLimit * AccountResource.__TotalEnergyWeight * Energy * 1_000_000)

    @staticmethod
    def GetSumForBandWidth(BandWidth: float) -> int:
        if AccountResource.__TotalNetLimit is None:
            raise Exception("未获取全网质押TRX")

        return int(1 / AccountResource.__TotalNetLimit * AccountResource.__TotalNetWeight * BandWidth * 1_000_000)