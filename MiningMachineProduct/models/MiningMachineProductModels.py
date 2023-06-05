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

from MiningMachineProduct.models.ComboModelModels import ComboModel
from MiningMachineProduct.models.ComboModels import Combo
from MiningMachineProduct.models.ComboPeriodModels import ComboPeriod
from MiningMachineProduct.models.MiningMachineSpecificationModels import MiningMachineSpecification


class MiningMachineProduct(models.Model):
    """
    矿机产品
    """
    comboId = models.ForeignKey(Combo, on_delete=models.PROTECT, help_text="套餐ID", verbose_name='套餐', db_column='comboId')
    comboPeriodId = models.ForeignKey(ComboPeriod, help_text="套餐周期ID", on_delete=models.PROTECT, verbose_name='套餐周期', db_column='comboPeriodId')
    comboModelId = models.ForeignKey(ComboModel, help_text="套餐模式ID", on_delete=models.PROTECT, verbose_name='套餐模式', db_column='comboModelId')
    miningMachineSpecificationId = models.ForeignKey(MiningMachineSpecification, help_text="矿机规格ID", on_delete=models.PROTECT, verbose_name='矿机规格', db_column='miningMachineSpecificationId')
    price = models.FloatField(help_text='价钱')

    class Meta:
        db_table = "MiningMachineProduct"
        verbose_name = '矿机产品'
        verbose_name_plural = '矿机产品'

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