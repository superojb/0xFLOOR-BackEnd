#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.db import models, connection
from rest_framework import serializers, exceptions
import django.utils.timezone as timezone

from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct
from Order.models.OrderModels import Order
from Order.models.OrderStatusModels import OrderStatus
from Tools.Mysql import Mysql
from django.contrib.auth import get_user_model

miningStatus_CHOICES = ((1, '等待上链'),(2, '待激活'),(3, '工作中'),(5, '暂停中'), (4, '已完成'))

class MinerBinding(models.Model):
    """
    矿机绑定
    """
    MinerBindingId = models.CharField(max_length=200, primary_key=True, help_text="订单绑定Id")
    orderId = models.ForeignKey(Order, on_delete=models.PROTECT, db_column='orderId', max_length=200, help_text="订单Id", verbose_name='订单Id')
    miningMachineProductId = models.ForeignKey(MiningMachineProduct, on_delete=models.PROTECT, db_column='miningMachineProductId', max_length=200, help_text="订单名称", verbose_name='订单名称')
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    minerAccount = models.CharField(max_length=200, help_text="机器链上账号", verbose_name='机器链上账号', null=True)
    miningStatusId = models.IntegerField(help_text="矿机状态Id", verbose_name='状态', choices=miningStatus_CHOICES)
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now, verbose_name='支付时间')
    updateTime = models.DateTimeField(help_text="更新时间", default=timezone.now, verbose_name='更新时间')

    class Meta:
        db_table = "MinerBinding"
        verbose_name = '矿机绑定'
        verbose_name_plural = '矿机绑定'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该订单！"})

    @staticmethod
    def Create(orderId: str) -> dict:
        cursor = connection.cursor()
        cursor.callproc('MinerBinding_Create', (orderId, ))
        result = Mysql.dictFetchAll(cursor)[0]
        Order.verifyMysqlResult(result)

        return result
