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
from rest_framework import permissions
from rest_auth.views import LoginView
from rest_framework.authentication import TokenAuthentication

from User.models.LoginLogsModels import LoginLogs
from Backend.settings import QQ_Map_API_Key

class Login(LoginView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

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

    def post(self, request, *args, **kwargs):
        response = super(Login, self).post(request, *args, **kwargs)
        user = TokenAuthentication().authenticate_credentials(response.data['key'])[0]
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        address = self.GetIpInfo(ip)
        print(ip, address)
        self.addLog(user.id, ip, address)
        return response