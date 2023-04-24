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


class MiningMachine(models.Model):
    """
    矿机
    """
    comboId = models.IntegerField(help_text="套餐ID")
    name = models.CharField(max_length=200, help_text="矿机名称")

    class Meta:
        db_table = "MiningMachine"

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