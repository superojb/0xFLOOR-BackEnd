#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.db import models, connection

from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct
from MiningMachineProduct.models.PledgeProfitRatioModels import PledgeProfitRatio
from Order.models.MinerBindingModels import MinerBinding, miningStatus_CHOICES
from Order.models.OrderModels import Order
from django.contrib.auth import get_user_model

from Tools.Mysql import Mysql


class MinerEarningsRecords(models.Model):
    """
    矿机绑定
    """
    MinerEarningsRecordsId = models.AutoField(primary_key=True, help_text="收益記錄Id")
    MinerBindingId = models.ForeignKey(MinerBinding, on_delete=models.PROTECT, db_column='MinerBindingId', max_length=200, help_text="機器綁定Id")
    orderId = models.ForeignKey(Order, on_delete=models.PROTECT, db_column='orderId', max_length=200, help_text="订单Id", verbose_name='订单Id')
    miningMachineProductId = models.ForeignKey(MiningMachineProduct, on_delete=models.PROTECT, db_column='miningMachineProductId', max_length=200, help_text="机器", verbose_name='机器')
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    minerAccount = models.CharField(max_length=200, help_text="机器链上账号", verbose_name='机器链上账号')
    miningStatusId = models.IntegerField(help_text="矿机状态Id", verbose_name='状态', choices=miningStatus_CHOICES)
    pledgeProfitRatioId = models.ForeignKey(PledgeProfitRatio, on_delete=models.PROTECT, db_column='pledgeProfitRatioId', help_text='质押', verbose_name='质押')
    MinerTotalRevenue = models.FloatField(help_text='機器總收益')
    MinerRevenueToday = models.FloatField(help_text='機器當天收益')
    UserRevenue = models.FloatField(help_text='機器總收益')
    electricity = models.IntegerField(help_text='剩余电量', verbose_name='剩余电量(天)')
    effectiveTime = models.IntegerField(help_text='有效时间', verbose_name='有效时间(天)')
    createTime = models.DateField(help_text="创建时间", auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = "MinerEarningsRecords"
        verbose_name = '礦機收益記錄'
        verbose_name_plural = '礦機收益記錄'

    @staticmethod
    def Settlement(MinerBindingId: str, state: str, revenue: float):
        cursor = connection.cursor()
        cursor.callproc('TransactionRecords_Settlement', (MinerBindingId, state, revenue))
        cursor.nextset()
