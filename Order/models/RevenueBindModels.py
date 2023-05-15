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

class OrderRevenueBind(models.Model):
    """
    订单收益绑定
    """
    orderId = models.CharField(primary_key=True, max_length=200, help_text="订单Id")
    RevenueAddressId = models.IntegerField()

    class Meta:
        db_table = "OrderRevenueBind"
        verbose_name = '收益绑定'
        verbose_name_plural = '收益绑定'

class OrderRevenueBindSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderRevenueBind
        fields = "__all__"