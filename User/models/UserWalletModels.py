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

class UserWallet(models.Model):
    """
    用户钱包
    """
    userWalletId = models.AutoField(primary_key=True)
    userId = models.IntegerField(help_text="用户ID")
    type = models.IntegerField(help_text='类别')
    address = models.CharField(max_length=200, help_text="登入地址")
    privateKey = models.CharField(max_length=200, help_text="钥匙")
    register = models.IntegerField(help_text="是否注册上链")

    class Meta:
        db_table = "UserWallet"
        verbose_name = '用户钱包'
        verbose_name_plural = '用户钱包'

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]

class UserWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = "__all__"