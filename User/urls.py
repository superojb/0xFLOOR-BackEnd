#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.urls import path, include, re_path
from User.Views.AccountConfirmEmail import AccountConfirmEmail
from User.Views.Frontend.LoginLogsAPIs import LoginLogsList
from User.Views.Frontend.RevenueAddressAPIs import RevenueAddressList, RevenueAddressAdd, RevenueAddressDelete, RevenueAddressUpdate
from User.Views.Login import Login
from User.Views.Frontend.UserAPIs import UserInfo, GetWallet, CashOutApply


urlpatterns = [
    re_path('frontend/rest-auth/login/', Login.as_view(), name='rest_login'),
    path('frontend/rest-auth/', include('rest_auth.urls')),

    path('frontend/rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^frontend/rest-auth/user-confirm-email/(?P<key>[-:\w]+)/$', AccountConfirmEmail, name='account_confirm_email'),
    re_path(r'^frontend/rest-auth/user-confirm-email/', AccountConfirmEmail, name='account_email_verification_sent'),

    path('frontend/login-logs-list/', LoginLogsList.as_view(), name='login-logs-list'),
    path('frontend/revenue-address-list/', RevenueAddressList.as_view(), name='revenue-address-list'),
    path('frontend/revenue-address-add/', RevenueAddressAdd.as_view(), name='revenue-address-add'),
    path('frontend/revenue-address-delete/', RevenueAddressDelete.as_view(), name='revenue-address-delete'),
    path('frontend/revenue-address-update/', RevenueAddressUpdate.as_view(), name='revenue-address-update'),

    path('frontend/user-info/', UserInfo.as_view(), name='user-info'),
    path('frontend/get_wallet/', GetWallet.as_view(), name='get_wallet'),
    path('frontend/cash_out_apply/', CashOutApply.as_view(), name='cash_out_apply'),
]
