#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.urls import path, include, re_path
from Order.Views.Frontend.OrderAPIs import OrderCreate, OrderList, OrderDetails
from Order.Views.Frontend.PaymentAPIs import getPaymentInfo, ConfirmPayment, ConfirmationOfTransactionAPI, GetBalance
from Order.Views.Frontend.MinerBindingAPIs \
    import MinerDetails, GetPledgeInfo, Pledge, \
    ConfirmationPledgeAPI, SettlementAPI, MinerOpenOrStop, ElectricityRecharge

urlpatterns = [
    path('frontend/create-order/', OrderCreate.as_view(), name='create-order'),
    path('frontend/order-list/', OrderList.as_view(), name='order-list'),
    path('frontend/order-details/', OrderDetails.as_view(), name='order-details'),
    path('frontend/get-payment-info/', getPaymentInfo.as_view(), name='get-payment-info'),
    path('frontend/get-balance/', GetBalance.as_view(), name='get-balance'),
    path('frontend/confirm-payment/', ConfirmPayment.as_view(), name='confirm-payment'),
    path('frontend/confirm-transaction/', ConfirmationOfTransactionAPI.as_view(), name='confirm-transaction'),

    path('frontend/miner-details/', MinerDetails.as_view(), name='miner-details'),
    path('frontend/miner-get-pledge-info/', GetPledgeInfo.as_view(), name='miner-get-pledge-info'),
    path('frontend/pledge/', Pledge.as_view(), name='pledge'),
    path('frontend/confirmation-pledge-api/', ConfirmationPledgeAPI.as_view(), name='confirmation-pledge-api'),
    path('frontend/settlement-api/', SettlementAPI.as_view(), name='settlement-api'),
    path('frontend/miner-open-or-stop/', MinerOpenOrStop.as_view(), name='miner-open-or-stop'),
    path('frontend/electricity-recharge/', ElectricityRecharge.as_view(), name='electricity-recharge'),
]
