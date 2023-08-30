#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：TransactionObj.py
@Author  ：MoJeffrey
@Date    ：2023/8/20 2:31 
"""
import copy

class TransactionObj:
    transaction_id: str = None
    _from: str = None
    to: dict = None
    value: float = None
    block_timestamp: str = None
    confirmed: bool = None
    recharge: bool = None
    associateId: str = None

    def __init__(self, data: dict):
        self.__dict__ = copy.deepcopy(data)
        self.value = int(self.value) / 1_000_000

    def GetDict(self):
        return self.__dict__