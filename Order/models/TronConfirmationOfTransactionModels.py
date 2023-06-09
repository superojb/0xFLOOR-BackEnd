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

RESULT_CHOICES = ((1, '已验证'),(0, '错误'),(2, '未验证'),)
TYPE_CHOICES = ((1, '注册账号'),(2, '代理'),(3, '转账'),(4, '取消代理'))

class TronConfirmationOfTransaction(models.Model):
    """
    Tron 交易确认任务
    """
    orderId = models.CharField(max_length=200, help_text="订单Id", db_index=True, verbose_name='订单Id')
    transactionId = models.CharField(max_length=200, help_text="交易id", verbose_name='交易id')
    type = models.IntegerField(help_text='类型', choices=TYPE_CHOICES, verbose_name='类别')
    result = models.IntegerField(help_text="结果", choices=RESULT_CHOICES, verbose_name='状态')
    response = models.TextField(help_text="结果回传")
    updateTime = models.DateTimeField(help_text="更新时间", auto_now=True, verbose_name='验证时间')
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now, verbose_name='创建时间')

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