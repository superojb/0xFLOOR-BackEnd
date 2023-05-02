#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from MiningMachineProduct.models.ComboModels import Combo, ComboSerializers

class ComboList(ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializers
    permission_classes = [permissions.AllowAny]

    swagger_tags = ['矿机产品']
    swagger = {
        "operation_summary": "Frontend 获取套餐List",
        "operation_description": "Frontend 获取套餐List",
        "tags": swagger_tags,
    }

    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
