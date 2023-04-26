#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.db import models, connection
from rest_framework import  serializers
import django.utils.timezone as timezone

class LoginLogs(models.Model):
    """
    登录记录
    """
    userId = models.IntegerField(help_text="用户ID")
    ip = models.GenericIPAddressField(help_text="登入IP")
    address = models.CharField(max_length=200, help_text="登入地址")
    createTime = models.DateTimeField(help_text="登入时间", default=timezone.now)

    class Meta:
        db_table = "LoginLogs"
        ordering = ['-createTime']
        verbose_name = '登录记录'
        verbose_name_plural = '登录记录'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class LoginLogsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LoginLogs
        fields = ['ip', 'address', 'createTime']