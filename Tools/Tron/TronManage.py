#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：TronManage.py
@Author  ：MoJeffrey
@Date    ：2023/5/11 16:57 
"""
import decimal
import json
from pprint import pprint

from tronpy.keys import PrivateKey
from tronpy import Tron
from tronpy.contract import Contract
from Tools.Tron.TronAPI import TronAPI
from Tools.Tron.models.AccountResource import AccountResource
from Tools.Tron.models.Transaction import Transaction
from Backend.settings import company_Tron_address, company_Tron_private_key_string, \
    Tron_network, usdt_contract_address, usdt_TransferBandWidthRequired, Tron_Web
from decimal import Decimal


class TronManage:
    tron = Tron(network=Tron_network)
    __Tron_API: TronAPI = TronAPI(tron)
    __Tron_Web: str = Tron_Web
    __company_Tron_address = company_Tron_address
    __company_Tron_private_key_string = company_Tron_private_key_string
    __company_Tron_private_key = PrivateKey(bytes.fromhex(__company_Tron_private_key_string))
    __usdt_contract_address = usdt_contract_address
    __usdt_contract = Contract(
        client=tron,
        addr=usdt_contract_address,
        abi=tron.get_contract(usdt_contract_address).abi
    )
    __USDTTransferBandWidthRequired = usdt_TransferBandWidthRequired

    def __init__(self):
        pass

    @staticmethod
    def Init():
        pass

    @staticmethod
    def GetTransactionDetailsURL(transactionId: str) -> str:
        return TronManage.__Tron_Web + "#/transaction/" + transactionId

    @staticmethod
    def GetUSDTBalance(address: str):
        balance = TronManage.__usdt_contract.functions.balanceOf(address)
        return Decimal(balance) / 1_000_000

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
    def Register(orderId: str, address: str):
        """
        注册
        :param orderId:
        :param address:
        :return:
        """

        Info = TronAPI.CreateAccount(orderId, TronManage.__company_Tron_address, address)
        T = Transaction(Info)
        T.sign(TronManage.__company_Tron_private_key)
        response = TronAPI.BroadcastTransaction(orderId, T.__dict__)

        if not ('result' in response and response['result'] == True):
            return False, ''

        return True, response['txid']

    @staticmethod
    def ConfirmationOfTransaction(orderId, TxId: str) -> dict:
        if TxId is None:
            return None
        return TronAPI.QueryTransaction(orderId, TxId)

    @staticmethod
    def GetIncome(orderId, TxId: str, Type: str):
        BandWidth = 0
        Energy = 0
        TRX = 0
        USDT = 0
        response = TronAPI.getTransactionInfoById(orderId, TxId)

        # 注册Tron 账号
        if Type == 'AccountCreateContract':
            TRX = - response['fee'] / 1_000_000
            BandWidth = - response['receipt']['net_usage']

        # 代理能量或宽带
        elif Type == 'DelegateResourceContract':
            BandWidth = - response['receipt']['net_usage']

        return BandWidth, Energy, TRX, USDT

    @staticmethod
    def GetUSDTTransferEnergyRequired(orderId, address, amount: decimal) -> int:
        return TronAPI.GetUSDTTransferEnergyRequired(orderId, TronManage.__company_Tron_address, address, int(amount * 1_000_000))

    @staticmethod
    def GetUSDTTransferBandWidthRequired() -> int:
        return TronManage.__USDTTransferBandWidthRequired

    @staticmethod
    def GetAccountResource(orderId, address):
        response = TronAPI.GetAccountResource(orderId, address)
        A = AccountResource(response)
        return A.GetCanUseEnergy(), A.GetCanUseBandWidth()

    @staticmethod
    def UnDelegate(orderId, address):
        """
        取消代理
        :return:
        """
        Info = TronAPI.GetDelegatedResourceV2(orderId, TronManage.__company_Tron_address, address)
        if 'delegatedResource' in Info:
            delegatedResource = Info['delegatedResource'][0]

            data = {
                "Identifier": orderId,
                "sender_addr": TronManage.__company_Tron_address,
                "recipient_addr": address,
                "balance": 0,
                "resource": ''
            }

            # 能量
            if 'frozen_balance_for_energy' in delegatedResource:
                energy = delegatedResource['frozen_balance_for_energy']
                data['balance'] = energy
                data['resource'] = 'ENERGY'

            # 宽带
            elif 'frozen_balance_for_bandwidth' in delegatedResource:
                bandwidth = delegatedResource['frozen_balance_for_bandwidth']
                data['balance'] = bandwidth
                data['resource'] = 'BANDWIDTH'

            if data['balance'] != 0:
                Info = TronAPI.UnDelegateResource(**data)
                if 'Error' in Info:
                    return 0, ''

                T = Transaction(Info)
                T.sign(TronManage.__company_Tron_private_key)
                response = TronAPI.BroadcastTransaction(orderId, T.__dict__)

                if not ('result' in response and response['result'] == True):
                    return 0, ''

                return 1, response['txid']

        return 2, ''

    @staticmethod
    def Delegate(orderId, address, balance, resource: str):
        """
        :param orderId:
        :param address:
        :param balance:
        :param resource: ENERGY | BANDWIDTH
        :return:
        """
        data = {
            "Identifier": orderId,
            "sender_addr": TronManage.__company_Tron_address,
            "recipient_addr": address,
            "balance": AccountResource.GetSumForEnergy(balance),
            "resource": resource
        }

        Info = TronAPI.DelegateResource(**data)
        if 'Error' in Info:
            return False, ''

        T = Transaction(Info)
        T.sign(TronManage.__company_Tron_private_key)
        response = TronAPI.BroadcastTransaction(orderId, T.__dict__)

        if not ('result' in response and response['result'] == True):
            return False, ''

        return True, response['txid']

    @staticmethod
    def USDTTransfer(orderId, address, amount: decimal, EnergyRequired: int, private_key):
        data = {
            "Identifier": orderId,
            "contract_address": TronManage.__usdt_contract_address,
            "sender_addr": address,
            "recipient_addr": TronManage.__company_Tron_address,
            "amount": int(amount * 1_000_000),
            "FeeLimit": AccountResource.GetFeeLimit(TronManage.GetUSDTTransferBandWidthRequired(), EnergyRequired)
        }

        Info = TronAPI.TriggerSmartContract(**data)
        if not ('result' in Info and Info['result']['result'] == True):
            return False, ''

        T = Transaction(Info['transaction'])
        T.sign(PrivateKey(bytes.fromhex(private_key)))
        response = TronAPI.BroadcastTransaction(orderId, T.__dict__)

        if not ('result' in response and response['result'] == True):
            return False, ''

        return True, response['txid']

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