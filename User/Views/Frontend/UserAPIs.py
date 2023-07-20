#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, exceptions, serializers
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, GenericAPIView
from User.models.LoginLogsModels import LoginLogsSerializers
from User.models.UserCashOutApplyModels import UserCashOutApply
from User.models.UserWalletModels import UserWallet

UserModel = get_user_model()


class CashOutApply(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 提现申请",
        "operation_description": "Frontend 提现申请",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['amount', 'currencyId', 'address']:
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
            "amount": request.data['amount'],
            "currencyId": request.data['currencyId'],
            "address": request.data['address']
        }

        return Response(UserCashOutApply.Apply(**data))

class GetWallet(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 获取钱包信息",
        "operation_description": "Frontend 获取钱包信息",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['currencyId']:
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

        return Response(UserWallet.GetWallet(self.request.user.id, request.data['currencyId']))

class UserInfo(GenericAPIView):
    serializer_class = LoginLogsSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET']

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 获取用户资料",
        "operation_description": "Frontend 获取用户资料",
        "tags": swagger_tags,
    }
    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(id=self.request.user.id)

        data = {
            'username': user.username,
            'email': user.email
        }
        return Response(data)
