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

from MiningMachineProduct.models.CurrencyModels import Currency
from Tools.Mysql import Mysql

TransactionRecords_Type = (
    (1, '提现'),
    (2, '质押'),
    (3, '解押'))


TransactionRecords_STATUS = (
    (0, '未确认'),
    (1, '已确认'),
    (2, '失败')
)

TransactionRecords_InitiationType = (
    (0, '矿机'),
    (1, '用户提现'),
)

class TransactionRecords(models.Model):
    """
    交易记录
    """
    transactionRecordsId = models.AutoField(primary_key=True, help_text="交易记录Id")
    type = models.IntegerField(help_text="交易类型", verbose_name='交易类型', choices=TransactionRecords_Type)
    initiationType = models.IntegerField(help_text="引发类型", choices=TransactionRecords_Type)
    initiationAssociateId = models.CharField(max_length=200, help_text="关联ID")
    disbursementsAddress = models.CharField(max_length=200, help_text="支出地址", verbose_name='支出地址')
    payeeAddress = models.CharField(max_length=200, help_text="收币地址", verbose_name='收币地址')
    amount = models.FloatField(help_text="交易数量", verbose_name='交易数量')
    currencyName = models.CharField(max_length=200, help_text="币名", verbose_name='币名')
    status = models.IntegerField(help_text="交易状态", verbose_name='交易状态', choices=TransactionRecords_STATUS)
    confirmationUrl = models.URLField(help_text="确认链URL")
    hax = models.CharField(max_length=200, help_text="交易Hax")
    note = models.TextField()
    coolingTime = models.DateTimeField(help_text="冷却到该时间", default=timezone.now)
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now)
    updateTime = models.DateTimeField(help_text="更新时间", default=timezone.now)

    class Meta:
        db_table = "TransactionRecords"
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
        ordering = ['-createTime']

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该机器！"})

    @staticmethod
    def GetPledgeTransaction(MinerBindingId: str, userId: int):
        cursor = connection.cursor()
        cursor.callproc('TransactionRecords_GetPledgeTransaction', (MinerBindingId, userId))
        result = Mysql.dictFetchAll(cursor)[0]
        TransactionRecords.verifyMysqlResult(result)

        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)
        if result:
            return result[0]['transactionRecordsId'], result[0]['hax'], result[0]['currencyName']
        else:
            return None, None, None
