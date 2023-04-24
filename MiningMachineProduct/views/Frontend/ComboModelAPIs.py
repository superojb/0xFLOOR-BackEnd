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
from MiningMachineProduct.models.ComboModelModels import ComboModel, ComboModelSerializers

class ComboModelList(generics.ListAPIView):
    queryset = ComboModel.objects.all()
    serializer_class = ComboModelSerializers
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Frontend 获取套餐模式List",
        operation_description="获取套餐模式List", )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
