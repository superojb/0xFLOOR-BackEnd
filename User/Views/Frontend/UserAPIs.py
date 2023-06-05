#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, GenericAPIView
from User.models.LoginLogsModels import LoginLogsSerializers


UserModel = get_user_model()

class UserInfo(GenericAPIView):
    serializer_class = LoginLogsSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET']

    swagger_tags = ['用户管理']
    swagger = {
        "operation_summary": "Frontend 获取用户资料",
        "operation_description": "Frontend 获取用户资料",
        "tags": swagger_tags,
    }
    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(id=self.request.user.id)

        data = {
            'username': user.username,
            'email': user.email
        }
        return Response(data)
