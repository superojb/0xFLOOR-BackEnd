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
from Tools.Mysql import Mysql

STATUS_CHOICES = ((1, '开启'),(0, '关闭'),(2, '禁售'),)

class Currency(models.Model):
    """
    货币
    """
    currencyId = models.AutoField(primary_key=True, help_text="货币ID")
    name = models.CharField(max_length=200, help_text="币名", verbose_name='币名')
    nickname = models.CharField(max_length=200, help_text="简称", verbose_name='币名')
    staticIncome = models.FloatField(help_text="静态收益", verbose_name='静态收益')
    status = models.IntegerField(help_text="状态", choices=STATUS_CHOICES, verbose_name='状态')
    imgUrl = models.CharField(max_length=500, help_text="Logo Url", verbose_name='Logo')
    ranking = models.IntegerField(verbose_name='排名', unique=True)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = "Currency"
        verbose_name = '货币'
        verbose_name_plural = '货币'
        ordering = ['ranking']

    def Status(self):
        format_td = ''

        if self.status == 1:
            format_td = format_html('<span style="padding:2px;background-color:green;color:white">开启</span>')
        elif self.status == 2:
            format_td = format_html('<span style="padding:2px;background-color:yellow;color:black">禁售</span>')
        elif self.status == 0:
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">关闭</span>')
        return format_td

    Status.short_description = "状态"

    def Logo(self):
        if self.imgUrl == "":
            return ""
        return format_html(f'<img style="height: 50px;width: 50px;margin: auto 10px;border-radius: 50px;" src="{ self.imgUrl }"/>')

    Logo.short_description = "Logo"

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})

    @staticmethod
    def UserCloudPowerList_CurrencyList(userId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserCloudPowerList_CurrencyList', (userId,))
        result = Mysql.dictFetchAll(cursor)[0]

        if Currency.verifyMysqlResult(result):
            cursor.nextset()
            return Mysql.dictFetchAll(cursor)

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class CurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['currencyId', 'name', 'nickname', 'staticIncome', 'imgUrl', 'status']


class CurrencyListFilter(django_filters.FilterSet):
    # 添加你要筛选的字段和筛选条件
    status = django_filters.Filter(lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Currency
        fields = ['status', 'name']
