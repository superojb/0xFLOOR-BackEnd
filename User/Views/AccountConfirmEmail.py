#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：AccountConfirmEmail.py
@Author  ：MoJeffrey
@Date    ：2023/4/26 20:14 
"""
from django.http import HttpResponseRedirect
from Backend.settings import ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL


def AccountConfirmEmail(request, key):
    return HttpResponseRedirect(ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL + f'?code={key}')