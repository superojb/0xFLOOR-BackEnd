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
import django.utils.timezone as timezone

from Order.models.OrderStatusModels import OrderStatus
from Tools.Mysql import Mysql
from django.contrib.auth import get_user_model

class Order(models.Model):
    """
    订单
    """
    orderId = models.CharField(primary_key=True, max_length=200, help_text="订单Id", verbose_name='订单Id')
    orderName = models.CharField(max_length=200, help_text="订单名称", verbose_name='订单名称')
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    orderStatusId = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, help_text="订单状态Id", verbose_name='状态', db_column='orderStatusId')
    createTime = models.DateTimeField(help_text="订单创建时间", default=timezone.now, verbose_name='下单时间')

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

    @staticmethod
    def GetList(userId: str):
        cursor = connection.cursor()
        cursor.callproc('Order_GetList', (userId, ))
        result = Mysql.dictFetchAll(cursor)[0]

        if Order.verifyMysqlResult(result):
            cursor.nextset()
            return Mysql.dictFetchAll(cursor)

    @staticmethod
    def UpdateStatus(orderId: str, statusId: int):
        O = Order.objects.get(orderId=orderId)
        O.orderStatusId = OrderStatus.objects.get(orderStatusId=statusId)
        O.save()

    @staticmethod
    def Create(userId: str, orderName: str,ItemIdList: list, ItemNumList: list, ItemTypeList: list) -> dict:
        cursor = connection.cursor()
        cursor.callproc('Order_Create', (userId, orderName, ','.join(ItemIdList),
                        ','.join(ItemNumList), ','.join(ItemTypeList)))
        result = Mysql.dictFetchAll(cursor)[0]

        Order.verifyMysqlResult(result)
        cursor.nextset()
        return Mysql.dictFetchAll(cursor)[0]

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderId', 'orderName', 'userId', 'orderStatusId', 'createTime']