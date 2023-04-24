#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from MiningMachineProduct.views.Frontend.ComboAPIs import ComboList
from MiningMachineProduct.views.Frontend.ComboModelAPIs import ComboModelList
from MiningMachineProduct.views.Frontend.ComboPeriodAPIs import ComboPeriodList
from MiningMachineProduct.views.Frontend.CurrencyAPIs import CurrencyList
from MiningMachineProduct.views.Frontend.MiningMachineAPIs import MiningMachineList
from MiningMachineProduct.views.Frontend.MiningMachineProducAPIs import MiningMachineProductList
from MiningMachineProduct.views.Frontend.MiningMachineSpecificationAPIs import MiningMachineSpecificationList


urlpatterns = [
    url('frontend/ComboList', csrf_exempt(ComboList.as_view()), name='combo-list'),
    url('frontend/ComboModelList', ComboModelList.as_view(), name='combo-model-list'),
    url('frontend/ComboPeriodList', ComboPeriodList.as_view(), name='combo-period-list'),
    url('frontend/CurrencyList', CurrencyList.as_view(), name='currency-list'),
    url('frontend/MiningMachineList', MiningMachineList.as_view(), name='mining-machine-list'),
    url('frontend/MiningMachineProductList', MiningMachineProductList.as_view(), name='mining-machine-product-list'),
    url('frontend/MiningMachineSpecificationList', MiningMachineSpecificationList.as_view(), name='mining-machine-specification-list'),

]
