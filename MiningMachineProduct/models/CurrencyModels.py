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


class Currency(models.Model):
    """
    货币
    """
    name = models.CharField(max_length=200, help_text="币名")
    nickname = models.CharField(max_length=200, help_text="简称")
    staticIncome = models.FloatField(help_text="静态收益")
    status = models.IntegerField(help_text="状态")
    imgUrl = models.CharField(max_length=500, help_text="Logo Url")

    class Meta:
        db_table = "Currency"

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class CurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"