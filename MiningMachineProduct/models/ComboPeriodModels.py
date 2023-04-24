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


class ComboPeriod(models.Model):
    """
    套餐周期
    """
    day = models.IntegerField(help_text="天数")

    class Meta:
        db_table = "ComboPeriod"

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class ComboPeriodSerializers(serializers.ModelSerializer):
    class Meta:
        model = ComboPeriod
        fields = "__all__"