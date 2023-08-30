#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
import django_filters
from django.db import models, connection
from rest_framework import serializers, exceptions
from django.utils.html import format_html

from MiningMachineProduct.models.CurrencyModels import Currency
from Tools.Mysql import Mysql
from django.core.validators import MinLengthValidator

CurrencyNetwork_status = (
    (1, '开启'),
    (2, '关闭'),
)

class CurrencyNetwork(models.Model):
    """
    货币网络
    """
    currencyNetworkId = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200, help_text="币名", verbose_name='币名')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='货币', db_column='currencyId')
    status = models.IntegerField(verbose_name='狀態', )

    class Meta:
        db_table = "CurrencyNetwork"
        verbose_name = '货币网络'
        verbose_name_plural = '货币网络'
