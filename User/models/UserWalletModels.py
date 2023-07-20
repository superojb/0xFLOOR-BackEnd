#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.db import models, connection
from rest_framework import serializers
from rest_framework import exceptions

from MiningMachineProduct.models.CurrencyModels import Currency
from Tools.Mysql import Mysql


class UserWallet(models.Model):
    """
    用户钱包
    """
    userWalletId = models.AutoField(primary_key=True)
    userId = models.IntegerField(help_text="用户ID")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='货币', db_column='currencyId')
    address = models.CharField(max_length=200, help_text="登入地址")
    privateKey = models.CharField(max_length=200, help_text="钥匙")
    register = models.IntegerField(help_text="是否注册上链")
    balance = models.FloatField(help_text="餘額", verbose_name='餘額')
    freeze = models.FloatField(help_text="凍結", verbose_name='凍結')
    thaw = models.FloatField(help_text="解凍", verbose_name='解凍')
    cashOut = models.FloatField(help_text="提现中", verbose_name='提现中')

    class Meta:
        db_table = "UserWallet"
        verbose_name = '用户钱包'
        verbose_name_plural = '用户钱包'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该机器！"})
        elif result['code'] == 3:
            raise exceptions.ValidationError(detail={"msg": "没有该币！"})

    @staticmethod
    def ChangeFreeze(transactionRecordsId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_ChangeFreeze', (transactionRecordsId))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)
        return result

    @staticmethod
    def GetWallet(userId: int, currencyId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('User_GetWallet', (userId, currencyId))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)
        cursor.nextset()
        return Mysql.dictFetchAll(cursor)

    @staticmethod
    def Create(userId: int, currencyId: int, address: str, privateKey: str, register: balance) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_Create', (userId, currencyId, address, privateKey, register))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)
        return result


class UserWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = "__all__"
