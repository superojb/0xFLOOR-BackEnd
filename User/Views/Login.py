#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：AccountConfirmEmail.py
@Author  ：MoJeffrey
@Date    ：2023/4/26 20:14 
"""
import json

import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, exceptions
from rest_auth.views import LoginView
from rest_framework.authentication import TokenAuthentication
from django.utils.translation import ugettext_lazy
from User.models.LoginLogsModels import LoginLogs
from Backend.settings import QQ_Map_API_Key
from rest_auth.app_settings import LoginSerializer
from django.contrib.auth import get_user_model

class TheLoginSerializer(LoginSerializer):
    UserModel = get_user_model()

    def _validate_email(self, email, password):
        """
        重新写一下，
        email注册
        :param email:
        :param password:
        :return:
        """
        if email and password:
            username = self.UserModel.objects.get(email__iexact=email).get_username()
            user = self.authenticate(username=username, password=password)
        else:
            msg = ugettext_lazy('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user


class Login(LoginView):
    serializer_class = TheLoginSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    Schema = openapi.Schema

    swagger_tags = ['用户管理']
    swagger_request_body = Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': Schema(type=openapi.TYPE_STRING, description='电邮地址'),
            'password': Schema(type=openapi.TYPE_STRING, description='密码')
        }
    )

    swagger_responses_200_examples = {'application/json': {'key': 'xxxxxx'}}
    swagger_responses_200_Schema = Schema(
        type=openapi.TYPE_OBJECT,
        required=['key'],
        properties={
            'key': Schema(type=openapi.TYPE_STRING, description='Token')
        }
    )
    swagger_responses_200 = openapi.Response(description='登入成功', schema=swagger_responses_200_Schema, examples=swagger_responses_200_examples)

    swagger_responses_400_examples = {'application/json': {'non_field_errors': ['Unable to log in with provided credentials.']}}
    swagger_responses_400_Schema = Schema(
        type=openapi.TYPE_OBJECT,
        required=['non_field_errors'],
        properties={
            'non_field_errors': Schema(
                type=openapi.TYPE_ARRAY,
                items=Schema(type=openapi.TYPE_STRING, description="失败原因"),
            )
        }
    )
    swagger_responses_400 = openapi.Response(description='登入失败 List中有失败原因', schema=swagger_responses_400_Schema, examples=swagger_responses_400_examples)
    swagger_responses = {
        400: swagger_responses_400,
        200: swagger_responses_200
    }

    swagger = {
        "operation_summary": "Frontend 客户登入",
        "operation_description": "Frontend 客户登入",
        "request_body": swagger_request_body,
        "responses": swagger_responses,
        "tags": swagger_tags,
    }

    def GetIpInfo(self, IP) -> str:
        url = f'https://apis.map.qq.com/ws/location/v1/ip?key={QQ_Map_API_Key}&ip={IP}'
        address = json.loads(requests.get(url).text)
        address = address['result'] if 'result' in address else address['message']

        if 'ad_info' in address:
            address = address['ad_info']['nation'] + address['ad_info']['city'] + address['ad_info']['district']
        return address

    def addLog(self, userId, ip, address):
        LoginLogs.objects.create(
            userId=userId,
            ip=ip,
            address=address
        )

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        response = super(Login, self).post(request, *args, **kwargs)

        user = TokenAuthentication().authenticate_credentials(response.data['key'])[0]
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        address = self.GetIpInfo(ip)
        self.addLog(user.id, ip, address)

        return response