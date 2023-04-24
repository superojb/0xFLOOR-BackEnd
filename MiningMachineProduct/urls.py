#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.conf.urls import url
from MiningMachineProduct.views.Frontend.CurrencyAPIs import CurrencyList

urlpatterns = [
    url('frontend/CurrencyList', CurrencyList.as_view(), name='currency-list')
]
