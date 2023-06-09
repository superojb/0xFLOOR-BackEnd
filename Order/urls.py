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
from Order.Views.Frontend.PaymentAPIs import getPaymentInfo, ConfirmPayment, ConfirmationOfTransactionAPI

urlpatterns = [
    path('frontend/create-order/', OrderCreate.as_view(), name='create-order'),
    path('frontend/order-list/', OrderList.as_view(), name='order-list'),
    path('frontend/get-payment-info/', getPaymentInfo.as_view(), name='get-payment-info'),
    path('frontend/confirm-payment/', ConfirmPayment.as_view(), name='confirm-payment'),
    path('frontend/confirm-transaction/', ConfirmationOfTransactionAPI.as_view(), name='confirm-transaction'),
]
