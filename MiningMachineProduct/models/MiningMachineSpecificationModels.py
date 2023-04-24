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


class MiningMachineProduct(models.Model):
    """
    矿机产品
    """
    comboId = models.IntegerField(help_text="套餐ID")
    comboPeriodId = models.IntegerField(help_text="套餐周期ID")
    comboModelId = models.IntegerField(help_text="套餐模式ID")
    miningMachineSpecificationId = models.IntegerField(help_text="矿机规格ID")
    price = models.FloatField(help_text='价钱')

    class Meta:
        db_table = "MiningMachineProduct"

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class MiningMachineProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = MiningMachineProduct
        fields = "__all__"