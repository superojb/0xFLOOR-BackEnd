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

from MiningMachineProduct.models.CurrencyModels import Currency


class Combo(models.Model):
    """
    套餐
    """
    name = models.CharField(max_length=200, help_text="套餐名称", verbose_name='套餐名称')
    currencyId = models.ForeignKey(Currency, on_delete=models.PROTECT, help_text="货币Id", verbose_name='货币', db_column='currencyId')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Combo"
        verbose_name = '套餐'
        verbose_name_plural = '套餐'

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