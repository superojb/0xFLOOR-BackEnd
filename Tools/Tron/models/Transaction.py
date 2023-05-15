#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：Transaction.py
@Author  ：MoJeffrey
@Date    ：2023/5/11 17:42 
"""
from tronpy.keys import PrivateKey


class Transaction:
    raw_data = None
    signature = None
    txID = None
    raw_data_hex = None

    def __init__(self, Object: dict = None):
        if Object is not None:
            self.__dict__ = Object.copy()

    def sign(self, private_key: PrivateKey):
        sig = private_key.sign_msg_hash(bytes.fromhex(self.txID))
        self.signature = [sig.hex()]
