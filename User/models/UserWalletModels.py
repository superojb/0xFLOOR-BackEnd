#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyModels.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:30 
"""
import copy
import traceback

from django.db import models, connection
from loguru import logger
from rest_framework import serializers
from rest_framework import exceptions

from MiningMachineProduct.models.CurrencyModels import Currency
from Order.models.TronRequestLogsModels import TronRequestLogs
from Tools.Mysql import Mysql
from Tools.Tron.TronAPI import TronAPI
from Tools.Tron.TronManage import TronManage
from Tools.common.TransactionObj import TransactionObj
from Backend.settings import UserWalletConfirmationOfTransaction_Log
from User.models.UserWalletLogModels import UserWalletLog, UserWalletLogStatus


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
    def verifyMysqlResult(result: dict, NeedRaise: bool = True) -> bool:
        Error = None
        if result['code'] == 0:
            return True
        elif result['code'] == 1:
            Error = exceptions.ValidationError(detail={"msg": "没有该用户！"})
        elif result['code'] == 2:
            Error = exceptions.ValidationError(detail={"msg": "没有该机器！"})
        elif result['code'] == 3:
            Error = exceptions.ValidationError(detail={"msg": "没有该币！"})
        elif result['code'] == 4:
            Error = exceptions.ValidationError(detail={"msg": "已有该交易！"})
        if NeedRaise:
            raise Error
        else:
            return False

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
    def GetWalletList(userId: int, limit: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('User_GetWalletList', (userId, limit))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)
        cursor.nextset()
        return Mysql.dictFetchAll(cursor)

    @staticmethod
    def GetRechargeInfo(userId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_GetRechargeInfo', (userId, ))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)

        Obj = {}
        cursor.nextset()
        Obj['currency'] = Mysql.dictFetchAll(cursor)
        cursor.nextset()
        Obj['network'] = Mysql.dictFetchAll(cursor)

        return Obj

    @staticmethod
    def GetWithdrawalsInfo(userId: int) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_GetWithdrawalsInfo', (userId,))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)

        Obj = {}
        cursor.nextset()
        Obj['currency'] = Mysql.dictFetchAll(cursor)
        cursor.nextset()

        Obj['network'] = Mysql.dictFetchAll(cursor)
        cursor.nextset()
        Obj['withdrawalsAddress'] = Mysql.dictFetchAll(cursor)

        return Obj

    @staticmethod
    def Create(userId: int, currencyId: int, address: str, privateKey: str, register: balance) -> dict:
        cursor = connection.cursor()
        cursor.callproc('UserWallet_Create', (userId, currencyId, address, privateKey, register))
        result = Mysql.dictFetchAll(cursor)[0]
        UserWallet.verifyMysqlResult(result)
        return result

    @staticmethod
    def balanceChange(userId: int, currencyId: int, Transaction: TransactionObj) -> bool:
        cursor = connection.cursor()

        params = (
            userId,
            currencyId,
            1 if Transaction.recharge else 2,
            2 if Transaction.confirmed else 1,
            Transaction.value,
            Transaction.transaction_id,
            Transaction.block_timestamp,
            Transaction.associateId if Transaction.associateId else ''
        )
        cursor.callproc('UserWallet_balanceChange', params)
        result = Mysql.dictFetchAll(cursor)[0]
        return UserWallet.verifyMysqlResult(result, NeedRaise=False)


class UserWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = "__all__"

class UnConfirmedTransaction:
    UserWalletLogId: int = None
    userId: str = None
    changeAmount: float = None
    type: int = None
    TransactionId: str = None
    CurrencyName: str = None

    def __init__(self, data: dict):
        self.__dict__ = copy.deepcopy(data)

    def GetDict(self):
        return self.__dict__

class UserWalletConfirmationOfTransaction:
    __TransactionInfo = None

    def __init__(self, TransactionInfo: UnConfirmedTransaction):
        self.__TransactionInfo = TransactionInfo
        print(self.__TransactionInfo.GetDict())

    def Do(self):
        if self.__TransactionInfo.CurrencyName == 'USDT':
            self.USDTConfirmation()

    def USDTConfirmation(self):
        response = TronManage.ConfirmationOfTransaction(self.__TransactionInfo.TransactionId, self.__TransactionInfo.TransactionId)

        # 成功
        if 'ret' in response and response['ret'][0]['contractRet'] == 'SUCCESS':
            UserWalletLog.ConfirmedTransaction(self.__TransactionInfo.UserWalletLogId)

        # 还在确认
        elif response == {}:
            return

        # 报错
        else:
            UW = UserWalletLog.objects.get(UserWalletLogId=self.__TransactionInfo.UserWalletLogId)
            UW.status = UserWalletLogStatus.fail.value
            UW.save()


def UserWalletConfirmationOfTransactionRun():
    logger.add(UserWalletConfirmationOfTransaction_Log, level="INFO", rotation="1 week")
    TronAPI.Log = TronRequestLogs.Create
    try:
        UnConfirmedList = UserWalletLog.GetUnConfirmedList()

        for Item in UnConfirmedList:
            UserWalletConfirmationOfTransaction(UnConfirmedTransaction(Item)).Do()

    except Exception as e:
        logger.info('发生错误，错误信息为：', e)
        logger.info(traceback.format_exc())
        return