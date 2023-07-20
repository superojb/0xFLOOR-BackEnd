#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：PaymentAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/5/19 19:10 
"""
import traceback

from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, exceptions, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from Backend.settings import RegularConfirmationOfTransaction_Log, company_Tron_address
from MiningMachineProduct.models.CurrencyModels import Currency
from Order.models.MinerBindingModels import MinerBinding
from Order.models.OrderModels import Order
from Order.models.OrderPaymentInfoModels import OrderPaymentInfoSerializers, OrderPaymentInfo
from Order.models.OrderStatusModels import OrderStatus
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


def GenerateUSDTUserWallet(userId: int) -> str:
    address, key = TronManage.GetNewAddress()
    try:
        C = Currency.objects.get(name='USDT')
    except Currency.DoesNotExist:
        raise exceptions.ValidationError(detail={"msg": "不支持USDT， 请联络管理员！"})

    print("USDT ID" + str(C.currencyId))
    UserWallet.Create(userId, C.currencyId, address, key, False)
    return address

class GetBalance(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 獲取指定貨幣的餘額",
        "operation_description": "Frontend 獲取指定貨幣的餘額",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['CurrencyName']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    def GetUSDTBalance(self):
        try:
            address = UserWallet.objects.get(type=1, userId=self.request.user.id).address
        except UserWallet.DoesNotExist:
            address = GenerateUSDTUserWallet(self.request.user.id)

        data = {
            'balance': TronManage.GetUSDTBalance(address),
            'address': address
        }
        return Response(data)

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()

        if request.data['CurrencyName'] == 'USDT':
            return self.GetUSDTBalance()
        else:
            raise exceptions.ValidationError(detail={"msg": "不支持！"})



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
            address = GenerateUSDTUserWallet(self.request.user.id)
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

        try:
            C = Currency.objects.get(name='USDT')
        except Currency.DoesNotExist:
            raise exceptions.ValidationError(detail={"msg": "不支持USDT， 请联络管理员！"})

        UW = UserWallet.objects.get(userId=self.request.user.id, currency=C)

        # 注册账号， 进入定时任务确认订单
        if UW.register:
            TronConfirmationOfTransaction.Create(result['orderId'], 'IsRegister', 1)
        else:
            if TronManage.IsRegister(UW.address):
                UW.register = True
                UW.save()
                txId = 'IsRegister'
            else:
                Register, txId = TronManage.Register(result['orderId'], UW.address)
                if not Register:
                    raise exceptions.ValidationError(detail={"msg": "发生致命错误请联系技术人员！"})

            TronConfirmationOfTransaction.Create(result['orderId'], txId, 1)

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
        try:
            logger.info("确定" + T.orderId)
            if not self.ConfirmationOfTransaction(T):
                return 2

            OrderId = T.orderId
            TheOrder = Order.objects.get(orderId=T.orderId)
            UserId = TheOrder.userId_id
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

                    Order.UpdateStatus(T.orderId, 5)
                    # 创建矿机绑定资料，等待后台管理员添加机器账号
                    if TheOrder.type == 1:
                        MinerBinding.Create(TC.orderId)
                    elif TheOrder.type == 2:
                        MinerBinding.AddElectricity(TC.orderId)
            return 0
        except Exception as e:
            TheOrder = Order.objects.get(orderId=T.orderId)
            TheOrder.orderStatusId = OrderStatus.objects.get(name='发生错误')
            TheOrder.note += '|' + '系统发生严重故障！请联络管理员！'
            TheOrder.save()
            raise e

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
        try:
            C = Currency.objects.get(name='USDT')
        except Currency.DoesNotExist:
            raise exceptions.ValidationError(detail={"msg": "不支持USDT， 请联络管理员！"})

        UW = UserWallet.objects.get(userId=userId, currency=C)
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
