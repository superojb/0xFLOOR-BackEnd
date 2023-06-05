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


class ComboModel(models.Model):
    """
    套餐模式
    """
    name = models.CharField(max_length=200, help_text="模式名称", verbose_name='模式名称')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ComboModel"
        verbose_name = '套餐模式'
        verbose_name_plural = '套餐模式'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class ComboModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ComboModel
        fields = "__all__"