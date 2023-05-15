#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：TronManage.py
@Author  ：MoJeffrey
@Date    ：2023/5/11 16:57 
"""
import json
from pprint import pprint

from tronpy.keys import PrivateKey
from tronpy import Tron

from Tools.Tron.TronAPI import TronAPI
from Tools.Tron.models.Transaction import Transaction


class TronManage:
    tron = Tron(network='nile')
    __Tron_API: TronAPI = TronAPI(tron)
    __company_Tron_address = 'TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA'
    __company_Tron_private_key_string = 'ca9e7b596a4df59c45b92b5c4ec788b35fac76e05ca435fc583d6662a34b8385'
    __company_Tron_private_key = PrivateKey(bytes.fromhex(__company_Tron_private_key_string))

    def __init__(self):
        pass

    @staticmethod
    def Init():
        pass
    
    @staticmethod
    def GetNewAddress():
        """
        会验证是否新地址
        :return:
        """
        while True:
            address, key = TronManage.GenerateAddress()
            if TronManage.IsRegister(address):
                continue
            return address, key

    @staticmethod
    def GenerateAddress():
        """
        创建账号， 还未验证是否已经存在
        :return:
        """
        usdt_address = TronManage.tron.generate_address()
        return usdt_address['base58check_address'], usdt_address['private_key']

    @staticmethod
    def IsRegister(address: str) -> bool:
        if TronAPI.GetAccount(address) == {}:
            return False
        return True

    @staticmethod
    def Register(address: str):
        Info = TronAPI.CreateAccount(TronManage.__company_Tron_address, address)
        T = Transaction(Info)
        T.sign(TronManage.__company_Tron_private_key)
        print(json.dumps(T.__dict__))

if __name__ == '__main__':
    pass
    # 创建地址
    print(TronManage().GetNewAddress())

    # 验证地址
    # Address = 'TH4P8ztMzkPW27JUyrSRqEV5BTBL3tPdtJ'
    # print(TronManage.IsRegister(Address))

    # 查询拥有可用的宽带和能量
    # a = TronAPI.GetAccountResource('TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA')
    # ar = AccountResource(a)
    # print(ar.GetCanUseEnergy())
    # print(ar.GetCanUseBandWidth())

    # 创建账号
    # Address = 'TH4P8ztMzkPW27JUyrSRqEV5BTBL3tPdtJ'
    # TronManage.Register(Address)