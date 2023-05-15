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
from Tools.Mysql import Mysql

class RevenueAddress(models.Model):
    """
    收益地址
    """
    userId = models.IntegerField(help_text="用户ID")
    currencyId = models.IntegerField(help_text="币种ID")
    address = models.CharField(max_length=200, help_text="收入地址")
    notes = models.CharField(max_length=200, help_text="备注")

    class Meta:
        db_table = "RevenueAddress"
        verbose_name = '收益地址'
        verbose_name_plural = '收益地址'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该币种！"})
        elif result['code'] == 3:
            raise exceptions.ValidationError(detail={"msg": "该地址已存在！"})
        elif result['code'] == 4:
            raise exceptions.ValidationError(detail={"msg": "该备注已存在！"})
        elif result['code'] == 5:
            raise exceptions.ValidationError(detail={"msg": "不能删除不是自己的收益地址！"})

    @staticmethod
    def GetList(userId: int, currencyId: int) -> list:
        cursor = connection.cursor()
        cursor.callproc('RevenueAddress_GetList', (userId, currencyId))
        result = Mysql.dictFetchAll(cursor)[0]

        if RevenueAddress.verifyMysqlResult(result):
            cursor.nextset()
            return Mysql.dictFetchAll(cursor)

    @staticmethod
    def Create(userId: int, currencyId: int, address: str, notes: str) -> dict:
        cursor = connection.cursor()
        cursor.callproc('RevenueAddress_Create', (userId, currencyId, address, notes))
        result = Mysql.dictFetchAll(cursor)[0]

        if RevenueAddress.verifyMysqlResult(result):
            return result

    @staticmethod
    def Delete(id: int, userId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('RevenueAddress_Delete', (id, userId))
        result = Mysql.dictFetchAll(cursor)[0]

        if RevenueAddress.verifyMysqlResult(result):
            return result

    @staticmethod
    def Update(id: int, userId: int, notes: str) -> dict:
        cursor = connection.cursor()
        cursor.callproc('RevenueAddress_Update', (id, userId, notes))
        result = Mysql.dictFetchAll(cursor)[0]

        if RevenueAddress.verifyMysqlResult(result):
            return result
class RevenueAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = RevenueAddress
        fields = ['address', 'notes']
