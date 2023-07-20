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
from Tools.Mysql import Mysql
from Tools.Tron.TronManage import TronManage


class OrderPaymentInfo(models.Model):
    """
    订单付款信息
    """
    orderId = models.CharField(primary_key=True, max_length=200, help_text="订单Id")
    type = models.IntegerField(help_text="支付虚拟币")
    price = models.DecimalField(help_text="价钱", max_digits=5, decimal_places=2)
    confirmationUrl = models.URLField(help_text="确认链URL")
    createTime = models.DateTimeField(help_text="订单创建时间", default=timezone.now)

    class Meta:
        db_table = "OrderPaymentInfo"
        verbose_name = '订单付款信息'
        verbose_name_plural = '订单付款信息'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "訂單錯誤！"})
        elif result['code'] == 3:
            raise exceptions.ValidationError(detail={"msg": "不支持USDT了！"})

    @staticmethod
    def GetOrderPaymentInfo(userId: str, orderId: str):
        cursor = connection.cursor()
        cursor.callproc('OrderPaymentInfo_GetInfo', (userId, orderId))
        result = Mysql.dictFetchAll(cursor)[0]

        if OrderPaymentInfo.verifyMysqlResult(result):
            cursor.nextset()
            return Mysql.dictFetchAll(cursor)[0]

    @staticmethod
    def Create(orderId: str, type: int, price: float, transactionId: str):
        O = OrderPaymentInfo()
        O.orderId = orderId
        O.type = type
        O.price = price
        O.confirmationUrl = TronManage.GetTransactionDetailsURL(transactionId)
        O.save()

class OrderPaymentInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentInfo
        fields = "__all__"