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
import django.utils.timezone as timezone
from rest_framework import exceptions
from enum import Enum, unique

from MiningMachineProduct.models.CurrencyModels import Currency
from Tools.Mysql import Mysql

@unique
class UserWalletLogType(Enum):
    recharge = 1
    withdraw = 2
    pledge = 3
    release = 4
    buy = 5


@unique
class UserWalletLogStatus(Enum):
    waitingConfirm = 1
    success = 2
    fail = 3
    application = 4

UserWalletLog_type = (
    (1, '充值'),
    (2, '提現'),
    (3, '質押'),
    (4, '解押'),
    (5, '购买'),
)

UserWalletLog_status = (
    (1, '等待確認'),
    (2, '成功'),
    (3, '失敗'),
    (4, '申请中')
)

class UserWalletLog(models.Model):
    """
    用户钱包日誌
    """
    UserWalletLogId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, help_text="用户ID", verbose_name='用户', db_column='userId')
    associateId = models.CharField(max_length=200, help_text="关联ID")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='货币', db_column='currencyId')
    type = models.IntegerField(verbose_name='類型', choices=UserWalletLog_type)
    changeAmount = models.FloatField(verbose_name='改變金額')
    hax = models.CharField(max_length=200, help_text="交易Hax")
    status = models.IntegerField(verbose_name='狀態', )
    balance = models.FloatField(verbose_name='餘額')
    transactionTime = models.BigIntegerField(help_text="交易時間")
    createTime = models.DateTimeField(help_text="記錄時間", default=timezone.now)
    updateTime = models.DateTimeField(help_text="更新時間", default=timezone.now)

    class Meta:
        db_table = "UserWalletLog"
        verbose_name = '用户钱包日誌'
        verbose_name_plural = '用户钱包日誌'

    @staticmethod
    def verifyMysqlResult(result: dict) -> bool:
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            raise exceptions.ValidationError(detail={"msg": "没有该用户！"})

    @staticmethod
    def GetWalletLogList(userId: int, currencyId: int, type: int, page: int, limit: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_GetUserWalletLogList', (userId, currencyId, type, page, limit))
        obj = {}
        obj['data'] = Mysql.dictFetchAll(cursor)

        cursor.nextset()
        obj['totalCount'] = Mysql.dictFetchAll(cursor)

        return obj

    @staticmethod
    def GetUnConfirmedList() -> list:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_GetUnConfirmedList', ())
        return Mysql.dictFetchAll(cursor)

    @staticmethod
    def ConfirmedTransaction(UserWalletLogId: int) -> list:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_ConfirmedTransaction', (UserWalletLogId, ))
        return Mysql.dictFetchAll(cursor)[0]