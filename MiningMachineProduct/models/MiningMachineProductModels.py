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


class MiningMachineSpecification(models.Model):
    """
    矿机规格
    """
    miningMachineId = models.IntegerField(help_text="矿机ID")
    specification = models.CharField(max_length=200, help_text="规格")

    class Meta:
        db_table = "MiningMachineSpecification"

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class MiningMachineSpecificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = MiningMachineSpecification
        fields = "__all__"