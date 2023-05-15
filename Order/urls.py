#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.urls import path, include, re_path
from Order.Views.Frontend.OrderAPIs import OrderCreate, OrderList


urlpatterns = [
    path('frontend/create-order/', OrderCreate.as_view(), name='create-order'),
    path('frontend/order-list/', OrderList.as_view(), name='order-list'),
]
