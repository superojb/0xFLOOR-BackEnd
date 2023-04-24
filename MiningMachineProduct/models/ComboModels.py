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


class Combo(models.Model):
    """
    套餐
    """
    name = models.CharField(max_length=200, help_text="套餐名称")
    currencyId = models.IntegerField(help_text="货币ID")

    class Meta:
        db_table = "Combo"

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class ComboSerializers(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = "__all__"