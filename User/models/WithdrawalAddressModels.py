#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
import pymysql
from django.db import models, connection
from rest_framework import serializers, exceptions

from MiningMachineProduct.models.CurrencyModels import Currency
from MiningMachineProduct.models.CurrencyNetworkModels import CurrencyNetwork
from Tools.Mysql import Mysql


class WithdrawalAddress(models.Model):
    """
    提币地址
    """
    userId = models.IntegerField(help_text="用户ID")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='货币', db_column='currencyId')
    currencyNetwork = models.ForeignKey(CurrencyNetwork, on_delete=models.PROTECT, verbose_name='网络', db_column='currencyNetworkId')
    address = models.CharField(max_length=200, help_text="收入地址")
    notes = models.CharField(max_length=200, help_text="备注")

    class Meta:
        db_table = "WithdrawalAddress"
        verbose_name = '提币地址'
        verbose_name_plural = '提币地址'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该币种！"})
        elif result['code'] == 3:
            raise exceptions.ValidationError(detail={"msg": "没有该网络！"})
        elif result['code'] == 4:
            raise exceptions.ValidationError(detail={"msg": "该地址已存在！"})
        elif result['code'] == 5:
            raise exceptions.ValidationError(detail={"msg": "错误的提现地址！"})

    @staticmethod
    def GetList(userId: int, currencyId: int, page: int, limit: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWithdrawalAddress_GetList', (userId, currencyId, page, limit))
        obj = {}
        obj['data'] = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        obj['totalCount'] = Mysql.dictFetchAll(cursor)

        return obj

    @staticmethod
    def Create(userId: int, currencyId: int, currencyNetworkId: int, address: str, notes: str):
        cursor = connection.cursor()
        cursor.callproc('UserWithdrawalAddress_Create', (userId, currencyId, currencyNetworkId, address, notes))
        result = Mysql.dictFetchAll(cursor)[0]
        WithdrawalAddress.verifyMysqlResult(result)
        return

    @staticmethod
    def Delete(userId: int, id: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWithdrawalAddress_Delete', (userId, id))
        result = Mysql.dictFetchAll(cursor)[0]

        if WithdrawalAddress.verifyMysqlResult(result):
            return result
