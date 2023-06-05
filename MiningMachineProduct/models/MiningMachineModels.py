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

from MiningMachineProduct.models.ComboModels import Combo


class MiningMachine(models.Model):
    """
    矿机
    """
    comboId = models.ForeignKey(Combo, on_delete=models.PROTECT, help_text="套餐Id", verbose_name='套餐', db_column='comboId')
    name = models.CharField(max_length=200, help_text="矿机名称", verbose_name='矿机名称')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "MiningMachine"
        verbose_name = '矿机'
        verbose_name_plural = '矿机'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class MiningMachineSerializers(serializers.ModelSerializer):
    class Meta:
        model = MiningMachine
        fields = "__all__"