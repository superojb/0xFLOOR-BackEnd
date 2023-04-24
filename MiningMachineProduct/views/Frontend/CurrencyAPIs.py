#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import permissions
from MiningMachineProduct.models.CurrencyModels import Currency, CurrencySerializers

class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Frontend 获取货币List",
        operation_description="获取货币List", )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
