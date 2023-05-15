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

class OrderItem(models.Model):
    """
    订单中的项目
    """
    orderItemId = models.AutoField(primary_key=True, help_text="订单项目Id")
    orderId = models.CharField(max_length=200, help_text="订单Id")
    productId = models.IntegerField(help_text="产品Id")
    productTypeId = models.IntegerField(help_text="产品类别Id")
    num = models.IntegerField(help_text="数量")
    price = models.DecimalField(help_text="价钱", max_digits=5, decimal_places=2)

    class Meta:
        db_table = "OrderItem"
        verbose_name = '订单中项目'
        verbose_name_plural = '订单中项目'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"