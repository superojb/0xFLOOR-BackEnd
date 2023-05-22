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


class TronConfirmationOfTransaction(models.Model):
    """
    Tron 交易确认任务
    """
    orderId = models.CharField(max_length=200, help_text="订单Id", db_index=True)
    transactionId = models.CharField(max_length=200, help_text="交易id")
    type = models.IntegerField(help_text='类型')
    result = models.IntegerField(help_text="结果")
    response = models.TextField(help_text="结果回传")
    updateTime = models.DateTimeField(help_text="更新时间", auto_now=True)
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now)

    class Meta:
        db_table = "TronConfirmationOfTransaction"
        verbose_name = 'Tron 交易确认任务'
        verbose_name_plural = 'Tron 交易确认任务'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        pass

    @staticmethod
    def Create(orderId: str, transactionId: str, type: int):
        T = TronConfirmationOfTransaction()
        T.orderId = orderId
        T.transactionId = transactionId
        T.type = type
        T.result = 2
        T.response = ""
        T.save()