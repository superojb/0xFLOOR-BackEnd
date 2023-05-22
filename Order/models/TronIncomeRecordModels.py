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
from Tools.Mysql import Mysql

class TronIncomeRecord(models.Model):
    """
    Tron 收入记录
    """
    orderId = models.CharField(max_length=200, help_text="订单Id", db_index=True)
    type = models.IntegerField(help_text='类型')
    num = models.DecimalField(help_text="数量", max_digits=5, decimal_places=2)
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now)

    class Meta:
        db_table = "TronIncomeRecord"
        verbose_name = 'Tron 收入记录'
        verbose_name_plural = 'Tron 收入记录'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        pass

    @staticmethod
    def Create(orderId: str, type: int, num: int):
        if num == 0:
            return

        T = TronIncomeRecord()
        T.orderId = orderId
        T.type = type
        T.num = num
        T.save()

class TronIncomeRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = TronIncomeRecord
        fields = "__all__"