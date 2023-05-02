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
from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct, MiningMachineProductSerializers

class MiningMachineProductList(generics.ListAPIView):
    queryset = MiningMachineProduct.objects.all()
    serializer_class = MiningMachineProductSerializers
    permission_classes = [permissions.AllowAny]

    swagger_tags = ['矿机产品']
    swagger = {
        "operation_summary": "Frontend 获取矿机产品List",
        "operation_description": "Frontend 获取矿机产品List",
        "tags": swagger_tags,
    }

    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
