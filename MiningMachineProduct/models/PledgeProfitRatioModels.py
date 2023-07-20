#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30
"""
from django.db import models, connection
from django.core.validators import MinValueValidator, MaxValueValidator

from MiningMachineProduct.models.CurrencyModels import Currency


class PledgeProfitRatio(models.Model):
    """
    质押获利比例
    """
    validators_ProfitRatio = [MinValueValidator(0, message='请输入0-100'), MaxValueValidator(100, message='请输入0-100')]

    pledgeProfitRatioId = models.AutoField(primary_key=True, help_text="质押获利比例Id")
    currencyId = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='货币', db_column='currencyId')
    PledgeNum = models.FloatField(help_text="质押数量", verbose_name='质押数量')
    ProfitRatio = models.IntegerField(help_text="获利比例", verbose_name='获利比例', validators=validators_ProfitRatio)

    class Meta:
        db_table = "PledgeProfitRatio"
        verbose_name = '质押获利比例'
        verbose_name_plural = '质押获利比例'
        ordering = ['pledgeProfitRatioId', 'ProfitRatio']

    def CurrencyName(self):
        return self.currencyId.name

    CurrencyName.short_description = "货币"

    def Ratio(self):
        return str(self.ProfitRatio) + '%'

    Ratio.short_description = "获利比例"

    def Pledge(self):
        return f'{str(self.PledgeNum)} {self.currencyId.name}'

    Pledge.short_description = "质押"

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]
