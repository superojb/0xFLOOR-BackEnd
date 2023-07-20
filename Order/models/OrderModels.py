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
from rest_framework import serializers, exceptions
import django.utils.timezone as timezone

from Order.models.OrderStatusModels import OrderStatus
from Tools.Mysql import Mysql
from django.contrib.auth import get_user_model

Order_Type = (
    (1, '礦機'),
    (2, '電費'),
    (3, '維修單'))

class OrderDetails:
    orderInfo: dict = None
    productList: List[dict] = None
    paymentInfo: dict = None

    def GetDict(self):
        return self.__dict__

class Order(models.Model):
    """
    订单

    note = 記錄內容 發生錯誤或者 其他的時候記錄
    """
    orderId = models.CharField(primary_key=True, max_length=200, help_text="订单Id", verbose_name='订单Id')
    type = models.IntegerField(help_text="訂單類型", choices=Order_Type)
    orderName = models.CharField(max_length=200, help_text="订单名称", verbose_name='订单名称')
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    orderStatusId = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, help_text="订单状态Id", verbose_name='状态', db_column='orderStatusId')
    createTime = models.DateTimeField(help_text="订单创建时间", default=timezone.now, verbose_name='下单时间')
    note = models.TextField()

    def __str__(self):
        return self.orderId

    class Meta:
        db_table = "Order"
        verbose_name = '订单'
        verbose_name_plural = '订单'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "错误的产品！"})
        elif result['code'] == 3:
            raise exceptions.ValidationError(detail={"msg": "产品数量不可为小于1！"})
        elif result['code'] == 4:
            raise exceptions.ValidationError(detail={"msg": "没有该订单"})
        elif result['code'] == 5:
            raise exceptions.ValidationError(detail={"msg": "质押选择错误！"})

    @staticmethod
    def GetList(userId: str, orderType: int, page: int, limit: int):
        cursor = connection.cursor()
        cursor.callproc('Order_GetList', (userId, orderType, page, limit))
        result = Mysql.dictFetchAll(cursor)[0]
        Order.verifyMysqlResult(result)

        cursor.nextset()
        Obj = {}
        Obj['totalRows'] = Mysql.dictFetchAll(cursor)[0]['totalRows']

        cursor.nextset()
        Obj['list'] = Mysql.dictFetchAll(cursor)
        return Obj

    @staticmethod
    def UpdateStatus(orderId: str, statusId: int):
        O = Order.objects.get(orderId=orderId)
        O.orderStatusId = OrderStatus.objects.get(orderStatusId=statusId)
        O.save()

    @staticmethod
    def Create(userId: str, orderName: str,ItemIdList: list, ItemNumList: list, ItemTypeList: list, pledgeProfitRatioId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('Order_Create', (userId, orderName, ','.join(ItemIdList),
                        ','.join(ItemNumList), ','.join(ItemTypeList), pledgeProfitRatioId))
        result = Mysql.dictFetchAll(cursor)[0]

        Order.verifyMysqlResult(result)
        cursor.nextset()
        return Mysql.dictFetchAll(cursor)[0]

    @staticmethod
    def GetDetails(orderId: str, userId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('Order_GetDetails', (orderId, userId))
        result = Mysql.dictFetchAll(cursor)[0]
        Order.verifyMysqlResult(result)

        Obj = OrderDetails()

        cursor.nextset()
        Obj.orderInfo = Mysql.dictFetchAll(cursor)[0]

        cursor.nextset()
        Obj.productList = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        Obj.paymentInfo = Mysql.dictFetchAll(cursor)[0]

        return Obj.GetDict()

    @staticmethod
    def CheckTimeout():
        cursor = connection.cursor()
        cursor.callproc('Order_CheckTimeout', ())
        cursor.nextset()
        return

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderId', 'orderName', 'userId', 'orderStatusId', 'createTime']