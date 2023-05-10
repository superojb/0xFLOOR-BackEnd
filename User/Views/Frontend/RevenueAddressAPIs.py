#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, exceptions
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from User.models.RevenueAddressModels import RevenueAddressSerializers, RevenueAddress


class RevenueAddressList(ListAPIView):
    serializer_class = RevenueAddressSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 收益地址列表",
        "operation_description": "Frontend 收益地址列表",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        if 'currencyId' not in self.request.data:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})
        return

    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        self.verifyRequest()
        result = RevenueAddress.GetList(self.request.user.id, request.data['currencyId'])
        return Response(result)


class RevenueAddressAdd(CreateAPIView):
    serializer_class = RevenueAddressSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 添加收益地址",
        "operation_description": "Frontend 添加收益地址",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['currencyId', 'address', 'notes']:
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
            "currencyId": request.data['currencyId'],
            "address": request.data['address'],
            "notes": request.data['notes'],
        }
        result = RevenueAddress.Create(**data)
        return Response(result)


class RevenueAddressDelete(GenericAPIView):
    serializer_class = RevenueAddressSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 删除收益地址",
        "operation_description": "Frontend 删除收益地址",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['id']:
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
            "id": request.data['id']
        }
        result = RevenueAddress.Delete(**data)
        return Response(result)


class RevenueAddressUpdate(GenericAPIView):
    serializer_class = RevenueAddressSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 更新收益地址",
        "operation_description": "Frontend 更新收益地址",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['id', 'notes']:
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
            "id": request.data['id'],
            "notes": request.data['notes'],
        }
        result = RevenueAddress.Update(**data)
        return Response(result)