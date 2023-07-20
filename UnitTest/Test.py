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

r = requests.get(url='https://api.polkaholic.io/tx/0xa25bc67d6cff1fce43a9ba065173a4eb444b69e1e569d2e3268d2f5cb07ab95f', json={})
print(r.text)