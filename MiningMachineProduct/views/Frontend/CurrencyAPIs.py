#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, exceptions, permissions
from MiningMachineProduct.models.CurrencyModels import Currency, CurrencySerializers, CurrencyListFilter
from rest_framework.response import Response


class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers
    filterset_class = CurrencyListFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]

    swagger_tags = ['矿机产品']
    swagger = {
        "operation_summary": "Frontend 获取货币List",
        "operation_description": "Frontend 获取货币List",
        "tags": swagger_tags,
    }

    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UserCloudPowerList_CurrencyList(generics.GenericAPIView):
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
        return

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        return Response(Currency.UserCloudPowerList_CurrencyList(self.request.user.id))