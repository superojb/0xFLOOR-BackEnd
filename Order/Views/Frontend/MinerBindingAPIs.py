#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44
"""
import traceback

from loguru import logger

from Backend.settings import RegularConfirmationPledge_Log, RegularSettlement_Log
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions, exceptions
from rest_framework.generics import GenericAPIView

from MiningMachineProduct.models.CurrencyModels import Currency
from Order.models.MinerBindingModels import MinerBinding, MinerPledgeInfo
from Order.models.MinerEarningsRecordsModels import MinerEarningsRecords
from Order.models.OrderModels import Order
from Order.models.OrderPaymentInfoModels import OrderPaymentInfo
from Order.models.TransactionRecordsModels import TransactionRecords
from Order.models.TronConfirmationOfTransactionModels import TronConfirmationOfTransaction
from Tools.Khala.KhalaMange import KhalaMange
from Tools.Tron.TronManage import TronManage
from User.models.UserWalletModels import UserWallet
import django.utils.timezone as timezone


class ElectricityRecharge(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 用戶充值礦機電力",
        "operation_description": "Frontend 用戶充值礦機電力",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId', 'Num']:
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
        Num = request.data['Num']
        MinerBindingId = request.data['MinerBindingId']
        userId = self.request.user.id
        data = {
            "userId": userId,
            "MinerBindingId": MinerBindingId
        }

        result = MinerBinding.GetDetails(**data)

        if Num < 1:
            raise exceptions.ValidationError(detail={"msg": "充值電力必須大於1天！"})

        if result['effectiveTime'] != -999 and Num > (result['effectiveTime'] - result['electricity']):
            raise exceptions.ValidationError(detail={"msg": "充值電力大於有效期！"})

        orderId = MinerBinding.CreateElectricityRecharge(MinerBindingId, userId, Num)['OrderId']
        PaymentInfo = OrderPaymentInfo.GetOrderPaymentInfo(userId, orderId)

        # 没有地址
        if PaymentInfo['address'] is None:
            raise exceptions.ValidationError(detail={"msg": "還沒有專屬地址！"})

        # 判断是否能交付金额
        balance = TronManage.GetUSDTBalance(PaymentInfo['address'])
        if balance < PaymentInfo['price']:
            raise exceptions.ValidationError(
                detail={"msg": "未能繳付账单！", "balance": balance, 'price': PaymentInfo['price']})

        TronConfirmationOfTransaction.Create(orderId, 'IsRegister', 1)
        Order.UpdateStatus(orderId, 2)
        return Response({'code': 0})

class MinerDetails(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 获取框架详情",
        "operation_description": "Frontend 获取框架详情",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId']:
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
            "MinerBindingId": request.data['MinerBindingId']
        }
        result = MinerBinding.GetDetails(**data)
        return Response(result)

class MinerOpenOrStop(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 暫停或開啟礦機",
        "operation_description": "Frontend 暫停或開啟礦機",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId', 'IsOpen']:
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
        MinerBindingId = request.data['MinerBindingId']
        data = {
            "userId": self.request.user.id,
            "MinerBindingId": MinerBindingId,
            "IsOpen": request.data['IsOpen'],
        }
        MinerStatus = MinerBinding.OpenOrStop(**data)

        if MinerStatus == 3:
            MB = MinerBinding.objects.get(MinerBindingId=MinerBindingId)
            response = KhalaMange.GetPhalaComputationSessions(MB.minerAccount, MinerBindingId)
            IsWork = KhalaMange.getPhalaComputationIsWork(response)
            if IsWork:
                MB.miningStatusId = 4
                MB.save()

        return Response({'code': '0'})

class GetPledgeInfo(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 获取质押信息",
        "operation_description": "Frontend 获取质押信息",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    def Run(self, MinerBindingId: str, result: MinerPledgeInfo):

        # Phala 的质押
        if result.Currency == 'Phala':
            if not result.address:
                address, key = KhalaMange.GenerateAddress(MinerBindingId)
                UserWallet.Create(self.request.user.id, result.currencyId, address, key, True)
                result.address = address

            result.Balance = KhalaMange.getBalance(result.address, MinerBindingId)

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        MinerBindingId = request.data['MinerBindingId']
        data = {
            "userId": self.request.user.id,
            "MinerBindingId": request.data['MinerBindingId']
        }
        result = MinerBinding.GetPledgeInfo(**data)

        try:
            self.Run(MinerBindingId, result)
            return Response(result.GetDict())
        except Exception as e:
            raise exceptions.ValidationError(detail={"msg": str(e)})

class Pledge(GenericAPIView):
    """
    质押
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 发起质押申请",
        "operation_description": "Frontend 发起质押申请",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @staticmethod
    def SaveTransactionRecords(MinerBindingId, disbursementsAddress, amount, currencyName, hax):
        TR = TransactionRecords()
        TR.type = 2
        TR.initiationType = 0
        TR.initiationAssociateId = MinerBindingId
        TR.disbursementsAddress = disbursementsAddress
        TR.payeeAddress = KhalaMange.GetCompanyAddress()
        TR.amount = amount
        TR.currencyName = currencyName
        TR.hax = hax
        TR.status = 0
        TR.confirmationUrl = ''
        TR.note = f'{MinerBindingId} 申請質押 {amount} {currencyName}'
        TR.save()

    def Run(self, MinerBindingId: str, result: MinerPledgeInfo):
        if result.Currency == "Phala":
            UW = UserWallet.objects.get(userId=self.request.user.id, currency_id=result.currencyId)
            amount = result.PledgeNum - KhalaMange.GetHandlingFee()
            Hax = KhalaMange.Transfer(KhalaMange.GetCompanyAddress(), UW.privateKey, amount, MinerBindingId)
            Pledge.SaveTransactionRecords(MinerBindingId, result.address, result.PledgeNum, 'Phala', Hax)

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        MinerBindingId = request.data['MinerBindingId']
        data = {
            "userId": self.request.user.id,
            "MinerBindingId": request.data['MinerBindingId']
        }
        result = MinerBinding.GetPledgeInfo(**data)

        # 获取账号余额
        if result.Currency == 'Phala':
            result.Balance = KhalaMange.getBalance(result.address, MinerBindingId)

        if result.type == 2:
            if result.status != 2:
                raise exceptions.ValidationError(detail={"msg": "請勿重複質押！"})

        if result.PledgeNum == 0:
            raise exceptions.ValidationError(detail={"msg": "無需發起質押！"})

        if result.Balance < result.PledgeNum:
            raise exceptions.ValidationError(detail={"msg": "账号余额不足以发起质押！"})

        try:
            self.Run(MinerBindingId, result)
        except Exception as e:
            raise exceptions.ValidationError(detail={"msg": str(e)})

        return Response({'code': 0})

class ConfirmationPledgeAPI(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 主動觸發確定質押（无需Call， 用于测试）",
        "operation_description": "Frontend 主動觸發確定質押（无需Call， 用于测试）",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId']:
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
            "MinerBindingId": request.data['MinerBindingId']
        }
        transactionRecordsId, hax, currencyName = TransactionRecords.GetPledgeTransaction(**data)

        if not hax:
            raise exceptions.ValidationError(detail={"msg": "沒有需要確認的質押！"})

        result = ConfirmationPledge().Do(TransactionRecords.objects.get(transactionRecordsId=transactionRecordsId))

        return Response({'result': result})

def RegularConfirmationPledge():
    """
    定期確認質押
    :return:
    """
    logger.add(RegularConfirmationPledge_Log, level="INFO", rotation="1 week")
    logger.info("進入")
    try:
        ConfirmationPledge().Run()

    except Exception as e:
        logger.info('发生错误，错误信息为：', e)
        logger.info(traceback.format_exc())
        return

class ConfirmationPledge:
    __ConfirmationList = []
    def __init__(self):
        self.__ConfirmationList = TransactionRecords.objects.filter(initiationType=0, type=2, status=0)

    def Run(self):
        for Item in self.__ConfirmationList:
            self.Do(Item)

    @staticmethod
    def PledgeSuccess(TR: TransactionRecords, confirmationUrl: str) -> str:
        TR.status = 1
        TR.confirmationUrl = confirmationUrl
        TR.updateTime = timezone.now()
        TR.save()

        return TR.initiationAssociateId

    @staticmethod
    def PledgeError(TR: TransactionRecords, msg: str):
        TR.status = 2
        TR.note += f'\t\n {msg}'
        TR.updateTime = timezone.now()
        TR.save()

    @staticmethod
    def StartMiner(MinerBindingId: str):
        MB = MinerBinding.objects.get(MinerBindingId =MinerBindingId)

        if MB.minerAccount:
            # 檢查是否在工作
            response = KhalaMange.GetPhalaComputationSessions(MB.minerAccount, MB.MinerBindingId)
            IsWork = KhalaMange.getPhalaComputationIsWork(response)
            MB.miningStatusId = 4 if IsWork else 3
        else:
            # 等待上鏈
            MB.miningStatusId = 1

        MB.updateTime = timezone.now()
        MB.save()

    def Do(self, TR: TransactionRecords) -> str:
        result = ''
        confirmationUrl = ''
        msg = ''
        confirm = False

        if TR.currencyName == 'Phala':
            confirm, msg = KhalaMange.confirmTransfer(TR.hax, str(TR.transactionRecordsId))
            confirmationUrl = KhalaMange.GetConfirmTransferURL(TR.hax) if confirm else ''

        if confirm:
            MinerBindingId = ConfirmationPledge.PledgeSuccess(TR, confirmationUrl)
            ConfirmationPledge.StartMiner(MinerBindingId)
            result = 'OK'
        elif msg:
            ConfirmationPledge.PledgeError(TR, msg)
            result = 'Error'

        return result

class Settlement:

    __minerList = []

    def __init__(self):
        self.__minerList = MinerBinding.objects.filter(miningStatusId__in=[4, 5, 8])

    def Run(self):
        for Item in self.__minerList:
            self.Do(Item)

    @staticmethod
    def Do(MB: MinerBinding):
        logger.info(f"结算 {MB.MinerBindingId}")
        response = KhalaMange.GetPhalaComputationSessions(MB.minerAccount, MB.MinerBindingId)
        Revenue = KhalaMange.GetPhalaComputationRevenue(response)
        MinerEarningsRecords.Settlement(MB.MinerBindingId, response['state'], Revenue)

class SettlementAPI(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 主動觸發結算（无需Call， 用于测试）",
        "operation_description": "Frontend 主動觸發結算（无需Call， 用于测试）",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['MinerBindingId']:
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
            MB = MinerBinding.objects.get(MinerBindingId=request.data['MinerBindingId'], userId=self.request.user.id)
            Settlement.Do(MB)
        except MinerBinding.DoesNotExist:
            raise exceptions.ValidationError(detail={"msg": "該礦機不存在！"})

        return Response({'result': 'OK'})


def RegularSettlement():
    """
    每天结算一次矿机
    :return:
    """
    logger.add(RegularSettlement_Log, level="INFO", rotation="1 week")
    logger.info("進入")
    try:
        Settlement().Run()
    except Exception as e:
        logger.info('发生错误，错误信息为：', e)
        logger.info(traceback.format_exc())
        return