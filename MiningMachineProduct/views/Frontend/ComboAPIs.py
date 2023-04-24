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
from rest_framework import generics
from MiningMachineProduct.models.ComboModels import Combo, ComboSerializers

class ComboList(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializers
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Frontend 获取套餐List",
        operation_description="获取套餐List", )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
