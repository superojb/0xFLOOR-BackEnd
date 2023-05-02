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
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from User.models.LoginLogsModels import LoginLogs, LoginLogsSerializers


class LoginLogsList(ListAPIView):
    serializer_class = LoginLogsSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 登入记录列表",
        "operation_description": "Frontend 登入记录列表",
        "tags": swagger_tags,
    }
    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return LoginLogs.objects.filter(userId=self.request.user.id)

