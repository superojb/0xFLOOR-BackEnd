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

KEY_CHOICES = (('ElectricityBill', '电费'),)

class MiningMachineSetting(models.Model):
    """
    矿机设置内容，e.g 电费
    """
    miningMachineSettingId = models.AutoField(primary_key=True, help_text="矿机设置Id")
    key = models.CharField(max_length=200, help_text="key", unique=True, verbose_name='配置名', choices=KEY_CHOICES)
    value = models.CharField(max_length=200, help_text="值", verbose_name='配置值')

    class Meta:
        db_table = "MiningMachineSetting"
        verbose_name = '矿机设置'
        verbose_name_plural = '矿机设置'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class MiningMachineSettingSerializers(serializers.ModelSerializer):
    class Meta:
        model = MiningMachineSetting
        fields = "__all__"