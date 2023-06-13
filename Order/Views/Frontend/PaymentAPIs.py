#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：PaymentAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/5/19 19:10 
"""
from datetime import datetime
import traceback

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, exceptions, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from Backend.settings import RegularConfirmationOfTransaction_Log, company_Tron_address
from Order.models.MinerBindingModels import MinerBinding
from Order.models.OrderModels import Order
from Order.models.OrderPaymentInfoModels import OrderPaymentInfoSerializers, OrderPaymentInfo
from Order.models.TronConfirmationOfTransactionModels import TronConfirmationOfTransaction
from Order.models.TronIncomeRecordModels import TronIncomeRecord
from Order.models.TronRequestLogsModels import TronRequestLogs
from Tools.Tron.TronAPI import TronAPI
from Tools.Tron.TronManage import TronManage
from Tools.Tron.models.AccountResource import AccountResource
from User.models.UserWalletModels import UserWallet
from loguru import logger


def RegularConfirmationOfTransaction():
    logger.add(RegularConfirmationOfTransaction_Log, level="INFO", rotation="1 week")
    logger.info("开始")

    try:
        response = TronAPI.GetAccountResource("Main", company_Tron_address)
        AccountResource(response)
        AccountResource.SetEnergyPrices(TronAPI.getEnergyPrices())
        AccountResource.SetBandWidthPrices(TronAPI.getBandWidthPrices())
        TronAPI.Log = TronRequestLogs.Create
        ConfirmationOfTransaction().Run()

    except Exception as e:
        logger.info('发生错误，错误信息为：', e)
        logger.info(traceback.format_exc())
        return

class getPaymentInfo(GenericAPIView):
    class getPaymentInfo_body(serializers.Serializer):
        orderId = serializers.CharField(label='訂單Id')
        status = serializers.CharField(label='訂單狀態')
        price = serializers.FloatField(label='訂單價錢')
        createTime = serializers.CharField(label='訂單創建時間')
        address = serializers.CharField(label='支付地址')
        balance = serializers.CharField(label='餘額')
        orderName = serializers.CharField(label='订单名称')

    serializer_class = OrderPaymentInfoSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 獲取對指定訂單付款信息",
        "operation_description": "Frontend 獲取對指定訂單付款信息",
        "request_body": getPaymentInfo_body,
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['orderId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        data = {
            "userId": self.request.user.id,
            "orderId": request.data['orderId']
        }
        result = OrderPaymentInfo.GetOrderPaymentInfo(**data)

        # 判斷是否需要創建新地址
        if result['address'] is None:
            address, key = TronManage.GetNewAddress()
            UW = UserWallet()
            UW.type = 1
            UW.userId = self.request.user.id
            UW.address = address
            UW.privateKey = key
            UW.register = False
            UW.save()

            result['address'] = address

        result['balance'] = TronManage.GetUSDTBalance(result['address'])

        return Response(result)


class ConfirmPayment(GenericAPIView):
    class getConfirmPayment_body(serializers.Serializer):
        orderId = serializers.CharField(label='訂單Id')
        status = serializers.CharField(label='訂單狀態')
        price = serializers.FloatField(label='訂單價錢')
        createTime = serializers.CharField(label='訂單創建時間')
        address = serializers.CharField(label='支付地址')
        balance = serializers.CharField(label='餘額')

    serializer_class = OrderPaymentInfoSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 確認訂單",
        "operation_description": "Frontend 確認訂單",
        "request_body": getConfirmPayment_body,
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['orderId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        data = {
            "userId": self.request.user.id,
            "orderId": request.data['orderId']
        }
        result = OrderPaymentInfo.GetOrderPaymentInfo(**data)

        # 判断订单是否在处理中
        if result['status'] != '未支付':
            raise exceptions.ValidationError(detail={"msg": "订单已在处理中！"})

        # 判断是否有地址
        if result['address'] is None:
            raise exceptions.ValidationError(detail={"msg": "還沒有專屬地址！"})

        # 判断是否能交付金额
        balance = TronManage.GetUSDTBalance(result['address'])
        if balance < result['price']:
            raise exceptions.ValidationError(detail={"msg": "未能繳付账单！", "balance": balance, 'price': result['price']})

        UW = UserWallet.objects.get(userId=self.request.user.id)

        # 注册账号， 进入定时任务确认订单
        if UW.register:
            TronConfirmationOfTransaction.Create(result['orderId'], 'IsRegister', 1)
        else:
            if TronManage.IsRegister(UW.address):
                UW.register = True
                UW.save()

            Register, txId = TronManage.Register(result['orderId'], UW.address)
            TronConfirmationOfTransaction.Create(result['orderId'], txId, 1)

            if not Register:
                raise exceptions.ValidationError(detail={"msg": "发生致命错误请联系技术人员！"})

        Order.UpdateStatus(result['orderId'], 2)
        return Response({'code': 0})


class ConfirmationOfTransaction:
    __ConfirmationList = []
    def __init__(self):
        self.__ConfirmationList = TronConfirmationOfTransaction.objects.filter(result=2)

    def Run(self):
        for Item in self.__ConfirmationList:
            self.Do(Item)

    def Do(self, T: TronConfirmationOfTransaction) -> int:
        logger.info("确定" + T.orderId)
        if not self.ConfirmationOfTransaction(T):
            return 2

        OrderId = T.orderId
        UserId = Order.objects.get(orderId=T.orderId).userId_id
        if T.type in [1, 2]:
            # 代理
            HaveProxy, result, NeedEnergy = ConfirmationOfTransaction.DelegateEnergyOrBandWidth(OrderId, UserId)

            # 转账
            if not HaveProxy:
                ConfirmationOfTransaction.TransactionUSDT(result, NeedEnergy, UserId)

        elif T.type in [3, 4]:
            data = {
                "userId": UserId,
                "orderId": OrderId
            }
            result = OrderPaymentInfo.GetOrderPaymentInfo(**data)

            # 取消代理
            HaveUnDelegate = ConfirmationOfTransaction.UnDelegate(result)
            if not HaveUnDelegate:
                # 储存支付确定信息
                TC = TronConfirmationOfTransaction.objects.get(orderId=OrderId, result=1, type=3)
                OrderPaymentInfo.Create(TC.orderId, 1, result['price'], TC.transactionId)

                # 创建矿机绑定资料，等待后台管理员添加机器账号
                MinerBinding.Create(TC.orderId)
                Order.UpdateStatus(T.orderId, 5)
        return 0

    @staticmethod
    def DelegateEnergyOrBandWidth(orderId, UserId):
        """
        代理宽带
        :param request:
        :return:
        """
        data = {
            "userId": UserId,
            "orderId": orderId
        }
        result = OrderPaymentInfo.GetOrderPaymentInfo(**data)

        NeedEnergy = TronManage.GetUSDTTransferEnergyRequired(result['orderId'], result['address'], result['price'])
        NeedBandWidth = TronManage.GetUSDTTransferBandWidthRequired()
        HaveEnergy, HaveBandWidth = TronManage.GetAccountResource(result['orderId'], result['address'])

        txId = None
        Delegate = None

        # 能量质押
        if NeedEnergy > HaveEnergy:
            data = {
                "orderId": result['orderId'],
                "address": result['address'],
                "balance": NeedEnergy - HaveEnergy,
                "resource": "ENERGY"
            }
            Delegate, txId = TronManage.Delegate(**data)
        else:
            if NeedBandWidth > HaveBandWidth:
                data = {
                    "orderId": result['orderId'],
                    "address": result['address'],
                    "balance": NeedBandWidth - HaveBandWidth,
                    "resource": "BANDWIDTH"
                }
                Delegate, txId = TronManage.Delegate(**data)

        if Delegate is None:
            return False, result, NeedEnergy
        else:
            if Delegate:
                TronConfirmationOfTransaction.Create(result['orderId'], txId, 2)
                return True, result, NeedEnergy
            else:
                Order.UpdateStatus(result['orderId'], 8)
                raise exceptions.ValidationError(detail={"msg": "发生致命错误！"})

    def ConfirmationOfTransaction(self, T: TronConfirmationOfTransaction) -> bool:
        """
        确认订单
        :param T:
        :return:
        """
        if T.transactionId == "IsRegister":
            T.response = "OK"
            T.result = 1
            T.save()
            return True

        response = TronManage.ConfirmationOfTransaction(T.orderId, T.transactionId)
        if 'ret' in response and response['ret'][0]['contractRet'] == 'SUCCESS':
            T.response = response
            T.result = 1
            T.save()

            SUCCESS = True
            contractType = response['raw_data']['contract'][0]['type']

            BandWidth, Energy, TRX, USDT = TronManage.GetIncome(T.orderId, T.transactionId, contractType)
            TronIncomeRecord.Create(T.orderId, 1, BandWidth)
            TronIncomeRecord.Create(T.orderId, 2, Energy)
            TronIncomeRecord.Create(T.orderId, 3, TRX)
            TronIncomeRecord.Create(T.orderId, 4, USDT)

        elif response == {}:
            return False

        else:
            T.response = response
            T.result = 0
            T.save()
            Order.UpdateStatus(T.orderId, 8)
            raise exceptions.ValidationError(detail={"msg": "发生致命错误！"})

        return SUCCESS

    @staticmethod
    def TransactionUSDT(result: dict, EnergyRequired: int, userId: int):
        """
        转账
        :param result:
        :param EnergyRequired:
        :param userId:
        :return:
        """
        UW = UserWallet.objects.get(userId=userId, type=1)
        data = {
            "orderId": result['orderId'],
            "address": UW.address,
            "amount": result['price'],
            "EnergyRequired": EnergyRequired,
            "private_key": UW.privateKey
        }
        Transfer, txId = TronManage.USDTTransfer(**data)

        if Transfer:
            TronConfirmationOfTransaction.Create(result['orderId'], txId, 3)
            return True
        else:
            Order.UpdateStatus(result['orderId'], 8)
            raise exceptions.ValidationError(detail={"msg": "发生致命错误！"})

    @staticmethod
    def UnDelegate(result: dict):
        UnDelegateCode, txId = TronManage.UnDelegate(result['orderId'], result['address'])
        if UnDelegateCode == 0:
            Order.UpdateStatus(result['orderId'], 8)
            raise exceptions.ValidationError(detail={"msg": "发生致命错误！"})
        elif UnDelegateCode == 1:
            TronConfirmationOfTransaction.Create(result['orderId'], txId, 4)
            return True
        else:
            return False

class ConfirmationOfTransactionAPI(GenericAPIView):
    serializer_class = OrderPaymentInfoSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 确认交易（无需Call， 用于测试）",
        "operation_description": "Frontend 确认交易（无需Call， 用于测试）",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['orderId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        try:
            T = TronConfirmationOfTransaction.objects.get(orderId=request.data['orderId'], result=2)
        except Exception:
            return Response({'code': 3})

        code = ConfirmationOfTransaction().Do(T)

        return Response({'code': code})
