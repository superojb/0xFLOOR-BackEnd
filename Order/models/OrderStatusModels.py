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
import django.utils.timezone as timezone

class OrderStatus(models.Model):
    """
    订单状态
    """
    orderStatusId = models.AutoField(primary_key=True, help_text="订单状态Id")
    name = models.CharField(max_length=200, help_text="状态")

    class Meta:
        db_table = "OrderStatus"
        verbose_name = '订单状态'
        verbose_name_plural = '订单状态'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class OrderStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = "__all__"