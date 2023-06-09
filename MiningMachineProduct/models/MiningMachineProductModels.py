#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from typing import List

from django.db import models, connection
from rest_framework import  serializers, exceptions

from MiningMachineProduct.models.ComboModelModels import ComboModel
from MiningMachineProduct.models.ComboModels import Combo
from MiningMachineProduct.models.ComboPeriodModels import ComboPeriod
from MiningMachineProduct.models.MiningMachineSpecificationModels import MiningMachineSpecification
from Tools.Mysql import Mysql

class MiningMachineProductListObj:
    comboList: List[dict] = None
    comboModelList: List[dict] = None
    comboPeriodList: List[dict] = None
    miningMachineSpecificationList: List[dict] = None
    miningMachineList: List[dict] = None
    productList: List[dict] = None

    def GetDict(self):
        return self.__dict__

class MiningMachineProduct(models.Model):
    """
    矿机产品
    """
    comboId = models.ForeignKey(Combo, on_delete=models.PROTECT, help_text="套餐ID", verbose_name='套餐', db_column='comboId')
    comboPeriodId = models.ForeignKey(ComboPeriod, help_text="套餐周期ID", on_delete=models.PROTECT, verbose_name='套餐周期', db_column='comboPeriodId')
    comboModelId = models.ForeignKey(ComboModel, help_text="套餐模式ID", on_delete=models.PROTECT, verbose_name='套餐模式', db_column='comboModelId')
    miningMachineSpecificationId = models.ForeignKey(MiningMachineSpecification, help_text="矿机规格ID", on_delete=models.PROTECT, verbose_name='矿机规格', db_column='miningMachineSpecificationId')
    price = models.FloatField(help_text='价钱')

    def __str__(self):
        return self.Name()

    class Meta:
        db_table = "MiningMachineProduct"
        verbose_name = '矿机产品'
        verbose_name_plural = '矿机产品'

    def Name(self):
        Name = f'[{self.comboModelId.name}]{self.miningMachineSpecificationId.miningMachineId.name}'
        Name += f' ({self.miningMachineSpecificationId.specification}/{self.comboPeriodId.Period()})'
        return Name

    Name.short_description = "矿机"
    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该货币！"})

    @staticmethod
    def GetList(currencyId: str):
        cursor = connection.cursor()
        cursor.callproc('MiningMachineProduct_GetList', (currencyId,))
        result = Mysql.dictFetchAll(cursor)[0]
        MiningMachineProduct.verifyMysqlResult(result)

        Obj = MiningMachineProductListObj()

        cursor.nextset()
        Obj.comboList = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        Obj.comboModelList = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        Obj.comboPeriodList = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        Obj.miningMachineSpecificationList = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        Obj.miningMachineList = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        Obj.productList = Mysql.dictFetchAll(cursor)

        return Obj.GetDict()

    @staticmethod
    def GetProduct(productId: str):
        cursor = connection.cursor()
        cursor.callproc('MiningMachineProduct_GetProduct', (productId,))
        result = Mysql.dictFetchAll(cursor)[0]
        MiningMachineProduct.verifyMysqlResult(result)

        cursor.nextset()
        return Mysql.dictFetchAll(cursor)

    @staticmethod
    def GetProductCount(InquireSQL):
        cursor = connection.cursor()
        CountSQL = "SELECT count(*) FROM (" + InquireSQL + ") AS A"

        cursor.execute(CountSQL)
        rst = cursor.fetchone()
        return rst[0]


class MiningMachineProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = MiningMachineProduct
        fields = "__all__"