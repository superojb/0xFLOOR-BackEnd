#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
from django.contrib.auth import get_user_model
from django.db import models, connection
from rest_framework import  serializers
from rest_framework import exceptions

from MiningMachineProduct.models.CurrencyModels import Currency
from Tools.Mysql import Mysql
import django.utils.timezone as timezone

UserCashOutApply_status = (
    (1, '申请中'),
    (2, '确认中'),
    (3, '已提现'))


class UserCashOutApply(models.Model):
    """
    用户提现申请
    """
    UserCashOutApplyId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    status = models.IntegerField(verbose_name='状态', choices=UserCashOutApply_status)
    currencyId = models.ForeignKey(Currency, on_delete=models.PROTECT, help_text="货币Id", verbose_name='货币', db_column='currencyId')
    address = models.CharField(max_length=200, verbose_name="提现地址")
    amount = models.FloatField(verbose_name='金额')
    hax = models.CharField(max_length=200, help_text="交易Hax")
    note = models.TextField()
    createTime = models.DateTimeField(help_text="创建时间", default=timezone.now, verbose_name='支付时间')
    updateTime = models.DateTimeField(help_text="更新时间", auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "UserCashOutApply"
        verbose_name = '用户提现申请'
        verbose_name_plural = '用户提现申请'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            raise exceptions.ValidationError(detail={"msg": "没有该机器！"})

    @staticmethod
    def Apply(userId: int, amount: float, currencyId: int, address: str) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserCashOutApply_Create', (userId, amount, currencyId, address))
        result = Mysql.dictFetchAll(cursor)[0]
        UserCashOutApply.verifyMysqlResult(result)
        return result
