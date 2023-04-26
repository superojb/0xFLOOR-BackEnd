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

    @swagger_auto_schema(
        operation_summary="Frontend 获取登录记录List",
        operation_description="获取登录记录List", )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return LoginLogs.objects.filter(userId=self.request.user.id)

