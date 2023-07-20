#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.db import models, connection
from rest_framework import exceptions
import django.utils.timezone as timezone

from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct
from MiningMachineProduct.models.PledgeProfitRatioModels import PledgeProfitRatio
from Order.models.OrderModels import Order
from Tools.Mysql import Mysql
from django.contrib.auth import get_user_model

miningStatus_CHOICES = (
    (1, '等待上链'),
    (2, '等待质押'),
    (3, '待激活'),
    (4, '準備工作中'),
    (5, '工作中'),
    (6, '已完成'),
    (7, '暂停中'),
    (8, '准备暂停中'),
    (9, '维修中'),
    (10, '等待支付维修费'))

class MinerPledgeInfo:
    Currency: str = None
    address: str = None
    Balance: dict = None
    PledgeNum: float = None
    type: int = None
    status: int = None
    coolingTime: str = None
    currencyId: int = None

    def GetDict(self):
        return self.__dict__

class MinerBinding(models.Model):
    """
    矿机绑定
    """
    MinerBindingId = models.CharField(max_length=200, primary_key=True, help_text="订单绑定Id")
    orderId = models.ForeignKey(Order, on_delete=models.PROTECT, db_column='orderId', max_length=200, help_text="订单Id", verbose_name='订单Id')
    miningMachineProductId = models.ForeignKey(MiningMachineProduct, on_delete=models.PROTECT, db_column='miningMachineProductId', max_length=200, help_text="机器", verbose_name='机器')
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    minerAccount = models.CharField(max_length=200, help_text="机器链上账号", verbose_name='机器链上账号', null=True)
    miningStatusId = models.IntegerField(help_text="矿机状态Id", verbose_name='状态', choices=miningStatus_CHOICES)
    pledgeProfitRatioId = models.ForeignKey(PledgeProfitRatio, on_delete=models.PROTECT, db_column='pledgeProfitRatioId', verbose_name='质押')
    electricity = models.IntegerField(help_text='剩余电量', verbose_name='剩余电量(天)')
    effectiveTime = models.IntegerField(help_text='有效时间', verbose_name='有效时间(天)')
    workingDay = models.IntegerField(help_text='已工作（天）')
    TotalRevenue = models.FloatField(help_text='總收益')
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now, verbose_name='支付时间')
    updateTime = models.DateTimeField(help_text="更新时间", default=timezone.now, verbose_name='更新时间')

    class Meta:
        db_table = "MinerBinding"
        verbose_name = '矿机绑定'
        verbose_name_plural = '矿机绑定'

    def PledgeProfitRatioString(self):
        if self.pledgeProfitRatioId.PledgeNum == 0:
            return f'无需质押/{self.pledgeProfitRatioId.ProfitRatio}%'
        else:
            return f'{self.pledgeProfitRatioId.PledgeNum} {self.pledgeProfitRatioId.CurrencyName()}/{self.pledgeProfitRatioId.ProfitRatio}%'
    PledgeProfitRatioString.short_description = '质押'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该机器！"})

    @staticmethod
    def Create(orderId: str) -> dict:
        cursor = connection.cursor()
        cursor.callproc('MinerBinding_Create', (orderId, ))
        result = Mysql.dictFetchAll(cursor)[0]
        Order.verifyMysqlResult(result)

        return result

    @staticmethod
    def OpenOrStop(MinerBindingId: str, userId: int, IsOpen: bool) -> int:
        cursor = connection.cursor()
        cursor.callproc('MiningMachine_OpenOrStop', (MinerBindingId, userId, IsOpen))
        result = Mysql.dictFetchAll(cursor)[0]
        MinerBinding.verifyMysqlResult(result)
        return result['status']

    @staticmethod
    def CreateElectricityRecharge(MinerBindingId: str, userId: int, num: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('MiningMachine_CreateElectricityRecharge', (userId, MinerBindingId, num))
        result = Mysql.dictFetchAll(cursor)[0]
        MinerBinding.verifyMysqlResult(result)
        cursor.nextset()
        return Mysql.dictFetchAll(cursor)[0]

    @staticmethod
    def AddElectricity(orderId: str) -> dict:
        cursor = connection.cursor()
        cursor.callproc('MiningMachine_AddElectricity', (orderId, ))
        result = Mysql.dictFetchAll(cursor)[0]
        MinerBinding.verifyMysqlResult(result)
        return result

    @staticmethod
    def GetDetails(MinerBindingId: str, userId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('MiningMachine_GetDetails', (MinerBindingId, userId))
        result = Mysql.dictFetchAll(cursor)[0]
        MinerBinding.verifyMysqlResult(result)

        cursor.nextset()
        Obj = Mysql.dictFetchAll(cursor)[0]

        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)
        Obj['Pledge'] = result[0] if result else {}

        return Obj

    @staticmethod
    def GetPledgeInfo(MinerBindingId: str, userId: int) -> MinerPledgeInfo:
        cursor = connection.cursor()
        cursor.callproc('MiningMachine_GetPledgeInfo', (MinerBindingId, userId))
        result = Mysql.dictFetchAll(cursor)[0]
        MinerBinding.verifyMysqlResult(result)

        Obj = MinerPledgeInfo()
        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)
        Obj.Currency = result[0]['Currency']
        Obj.PledgeNum = result[0]['PledgeNum']
        Obj.currencyId = result[0]['currencyId']

        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)
        Obj.address = result[0]['address'] if result else None

        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)
        Obj.type = result[0]['type'] if result else None
        Obj.status = result[0]['status'] if result else None
        Obj.coolingTime = result[0]['coolingTime'] if result else None

        return Obj