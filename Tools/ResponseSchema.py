#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：ResponseSchema.py
@Author  ：MoJeffrey
@Date    ：2023/5/15 19:44 
"""
from rest_framework import permissions, exceptions, serializers

class ResponseSchemaCode(serializers.Serializer):
    code = serializers.CharField(label='id')

class ResponseSchemaMsg(serializers.Serializer):
    msg = serializers.CharField(label='信息')