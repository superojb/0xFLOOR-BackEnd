#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.db import models, connection
from rest_framework import serializers, exceptions
from Tools.Mysql import Mysql

from MiningMachineProduct.models.ComboModels import Combo


class MiningMachine(models.Model):
    """
    矿机
    """
    comboId = models.ForeignKey(Combo, on_delete=models.PROTECT, help_text="套餐Id", verbose_name='套餐', db_column='comboId')
    name = models.CharField(max_length=200, help_text="矿机名称", verbose_name='矿机名称')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "MiningMachine"
        verbose_name = '矿机'
        verbose_name_plural = '矿机'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该货币！"})

    @staticmethod
    def UserCloudPowerList_MinerList(userId: int, currencyId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserCloudPowerList_MinerList', (userId, currencyId))
        result = Mysql.dictFetchAll(cursor)[0]
        MiningMachine.verifyMysqlResult(result)

        Obj = {
            'previousAllTotalRevenue': 0,
            'AllTotalRevenue': 0,
        }

        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)
        Obj['MinerList'] = result

        cursor.nextset()
        result = Mysql.dictFetchAll(cursor)

        if result:
            Obj['previousAllTotalRevenue'] = result[0]['previousAllTotalRevenue']
            Obj['AllTotalRevenue'] = result[0]['AllTotalRevenue']

        return Obj


class MiningMachineSerializers(serializers.ModelSerializer):
    class Meta:
        model = MiningMachine
        fields = "__all__"