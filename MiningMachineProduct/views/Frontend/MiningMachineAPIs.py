#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, exceptions, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from MiningMachineProduct.models.MiningMachineModels import MiningMachine, MiningMachineSerializers

class MiningMachineList(generics.ListAPIView):
    queryset = MiningMachine.objects.all()
    serializer_class = MiningMachineSerializers
    permission_classes = [permissions.AllowAny]

    swagger_tags = ['矿机产品']
    swagger = {
        "operation_summary": "Frontend 获取矿机List",
        "operation_description": "Frontend 获取矿机List",
        "tags": swagger_tags,
    }

    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserCloudPowerList_MinerList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 用户获取共享算力中的货币列表",
        "operation_description": "Frontend 用户获取共享算力中的货币列表",
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
        return Response(MiningMachine.UserCloudPowerList_MinerList(self.request.user.id, request.data['currencyId']))