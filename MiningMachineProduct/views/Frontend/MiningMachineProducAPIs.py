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
from rest_framework.response import Response
from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct, MiningMachineProductSerializers

class MiningMachineProductList(generics.GenericAPIView):
    queryset = MiningMachineProduct.objects.all()
    serializer_class = MiningMachineProductSerializers
    permission_classes = [permissions.AllowAny]
    allowed_methods = ['GET']

    swagger_tags = ['矿机产品']
    swagger = {
        "operation_summary": "Frontend 获取矿机产品List",
        "operation_description": "Frontend 获取矿机产品List",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['currencyId']:
            if Item not in self.request.query_params:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})


    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        self.verifyRequest()

        return Response(MiningMachineProduct.GetList(request.query_params['currencyId']))

class GetPrdocut(generics.GenericAPIView):
    serializer_class = MiningMachineProductSerializers
    permission_classes = [permissions.AllowAny]
    allowed_methods = ['GET']

    swagger_tags = ['矿机产品']
    swagger = {
        "operation_summary": "Frontend 获取指定产品信息",
        "operation_description": "Frontend 获取指定产品信息",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['productId']:
            if Item not in self.request.query_params:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})


    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        self.verifyRequest()

        return Response(MiningMachineProduct.GetProduct(request.query_params['productId']))
