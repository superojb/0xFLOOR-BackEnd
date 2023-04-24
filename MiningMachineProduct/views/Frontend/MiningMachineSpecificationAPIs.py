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
from MiningMachineProduct.models.MiningMachineSpecificationModels import MiningMachineSpecification, MiningMachineSpecificationSerializers

class MiningMachineSpecificationList(generics.ListAPIView):
    queryset = MiningMachineSpecification.objects.all()
    serializer_class = MiningMachineSpecificationSerializers
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Frontend 获取矿机规格List",
        operation_description="获取矿机规格List", )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
