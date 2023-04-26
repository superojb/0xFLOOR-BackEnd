#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.conf.urls import url
from MiningMachineProduct.views.Frontend.ComboAPIs import ComboList
from MiningMachineProduct.views.Frontend.ComboModelAPIs import ComboModelList
from MiningMachineProduct.views.Frontend.ComboPeriodAPIs import ComboPeriodList
from MiningMachineProduct.views.Frontend.CurrencyAPIs import CurrencyList
from MiningMachineProduct.views.Frontend.MiningMachineAPIs import MiningMachineList
from MiningMachineProduct.views.Frontend.MiningMachineProducAPIs import MiningMachineProductList
from MiningMachineProduct.views.Frontend.MiningMachineSpecificationAPIs import MiningMachineSpecificationList


urlpatterns = [
    url('frontend/combo-list/', ComboList.as_view(), name='combo-list'),
    url('frontend/combo-model-list/', ComboModelList.as_view(), name='combo-model-list'),
    url('frontend/combo-period-list/', ComboPeriodList.as_view(), name='combo-period-list'),
    url('frontend/currency-list/', CurrencyList.as_view(), name='currency-list'),
    url('frontend/mining-machine-list/', MiningMachineList.as_view(), name='mining-machine-list'),
    url('frontend/mining-machine-product-list/', MiningMachineProductList.as_view(), name='mining-machine-product-list'),
    url('frontend/mining-machine-specification-list/', MiningMachineSpecificationList.as_view(), name='mining-machine-specification-list'),

]
