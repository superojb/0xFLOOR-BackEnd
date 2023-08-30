#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：Test.py
@Author  ：MoJeffrey
@Date    ：2023/5/28 6:52 
"""
from datetime import datetime

import requests

r = requests.get(url='https://nile.trongrid.io/v1/accounts/TUnRuN7uwU4obDoJhX6bYKT2dR8ef7qzou/transactions/trc20', params={'limit': 100, 'contract_address': 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj', 'only_unconfirmed': True})
print(r.text)