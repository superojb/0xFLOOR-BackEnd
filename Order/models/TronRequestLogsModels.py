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

class TronRequestLogs(models.Model):
    """
    Tron 场请求Logs
    """
    orderId = models.CharField(max_length=200, help_text="订单Id", db_index=True)
    url = models.URLField(help_text="请求URL")
    params = models.TextField(help_text="请求参数")
    response = models.TextField(help_text="结果回传")
    type = models.IntegerField(help_text='类型')
    createTime = models.DateTimeField(help_text="请求时间", default=timezone.now)

    class Meta:
        db_table = "TronRequestLogs"
        verbose_name = 'Tron 场请求Logs'
        verbose_name_plural = 'Tron 场请求Logs'
        ordering = ['-createTime']

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        pass

    @staticmethod
    def Create(url: str, orderId: str, params: dict, response: dict, type: int):
        T = TronRequestLogs()
        T.orderId = orderId
        T.url = url
        T.params = params
        T.response = response
        T.type = type
        T.save()

class TronRequestLogsSerializers(serializers.ModelSerializer):
    class Meta:
        model = TronRequestLogs
        fields = "__all__"