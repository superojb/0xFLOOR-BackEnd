#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：WithdrawalAddressAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/8/20 21:45 
"""
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, exceptions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from User.models.WithdrawalAddressModels import WithdrawalAddress


class WithdrawalAddressDelete(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 删除地址",
        "operation_description": "Frontend 删除地址",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['withdrawalAddressId']:
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
        return Response(WithdrawalAddress.Delete(self.request.user.id, request.data['withdrawalAddressId']))


class WithdrawalAddressCreate(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 新增提现地址",
        "operation_description": "Frontend 新增提现地址",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['currencyId', 'currencyNetworkId', 'notes', 'address']:
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
        currencyId = request.data['currencyId']
        currencyNetworkId = request.data['currencyNetworkId']
        notes = request.data['notes']
        address = request.data['address']
        WithdrawalAddress.Create(self.request.user.id, currencyId, currencyNetworkId, notes, address)
        return Response({'code': 0})


class GetWithdrawalAddressList(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 获取提现地址列表",
        "operation_description": "Frontend 获取提现地址列表",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['limit', 'page', 'currencyId']:
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
        currencyId = request.data['currencyId']
        page = request.data['page']
        limit = request.data['limit']
        return Response(WithdrawalAddress.GetList(self.request.user.id, currencyId, page, limit))

