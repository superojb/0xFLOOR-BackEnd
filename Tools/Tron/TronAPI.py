#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：Tron.py
@Author  ：MoJeffrey
@Date    ：2023/5/10 20:15 
"""
import requests
from tronpy.abi import trx_abi
from tronpy import Tron
from tronpy.keys import PrivateKey
from loguru import logger

from Tools.Tron.Exception.TronAPIRequestError import TronAPIRequestError

class TronAPI:
    __base_url = 'https://nile.trongrid.io/'
    __USDT_contract_address = 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj'
    __client = None
    __contract = None

    def __init__(self, tron: Tron):
        TronAPI.__client = tron
        TronAPI.__contract = TronAPI.__client.get_contract(TronAPI.__USDT_contract_address)

    @staticmethod
    def Requests(URL: str, params: dict, Identifier: str, Post: bool = True) -> dict:
        """
        :param URL:
        :param params:
        :param Type:
        :param Identifier: 识别码。为了追踪日志
        :return:
        """
        kwargs = {
            "url": URL,
            "json": params,
        }
        response = requests.post(**kwargs) if Post else requests.get(**kwargs)
        if response.status_code == 200:
            responseData = response.json()
            TronAPI.Log(URL, Identifier, params, responseData)
            return responseData

        raise TronAPIRequestError(URL, params, Identifier)

    @staticmethod
    def Log(URL: str, Identifier: str, params: dict, response: dict):
        logger.info(f"URL: {URL}; Identifier: {Identifier}; params: {params}; response: {response}")

    def getEnergyPrices(self) -> int:
        response = requests.get(f'{TronAPI.__base_url}wallet/getenergyprices')
        if response.status_code == 200:
            data = response.json()
            return int(data['prices'].split(',')[-1].split(':')[1])

    def getBandWidthPrices(self) -> int:
        response = requests.get(f'{TronAPI.__base_url}wallet/getbandwidthprices')
        if response.status_code == 200:
            data = response.json()
            return int(data['prices'].split(',')[-1].split(':')[1])

    def GetUSDTTransferEnergyRequired(self, sender_addr: str, recipient_addr: str, amount: int) -> int:
        raw = trx_abi.encode_single("(address,uint256)", [recipient_addr, amount])
        params = {
            "owner_address": sender_addr,
            "contract_address": TronAPI.__USDT_contract_address,
            "function_selector": "transfer(address,uint256)",
            "parameter": raw.hex(),
            "visible": True
        }

        response = requests.post(f'{TronAPI.__base_url}wallet/estimateenergy', json=params)

        if response.status_code == 200:
            data = response.json()
            return int(data['energy_required'])

    def GetFeeLimitOfUSDTTransfer(self, sender_addr: str, recipient_addr: str, amount: int):
        BandWidth = 345
        EnergyPrices = self.getEnergyPrices()
        BandWidthPrices = self.getBandWidthPrices()
        USDTTransferEnergyRequired = self.GetUSDTTransferEnergyRequired(sender_addr, recipient_addr, amount)
        return BandWidth * BandWidthPrices + EnergyPrices * USDTTransferEnergyRequired

    def DelegateResource(self,
                         private_key: str,
                         sender_addr: str,
                         recipient_addr: str,
                         balance: int,
                         resource: str = 'ENERGY') -> str:
        """
        把能量代理过去
        :param private_key:
        :param sender_addr:
        :param recipient_addr:
        :param balance:
        :param resource:
        :return:
        """
        Private_key = PrivateKey(bytes.fromhex(private_key))

        txn = (
            TronAPI.__client.trx.delegate_resource(owner=sender_addr, receiver=recipient_addr, balance=balance, resource=resource)
            .build()
            .sign(Private_key)
        )
        txn.broadcast().wait()
        return txn.txid

    def UndelegateResource(self,
                         private_key: str,
                         sender_addr: str,
                         recipient_addr: str,
                         balance: int,
                         resource: str = 'ENERGY') -> str:
        """
        把取消能量代理过去
        :param private_key:
        :param sender_addr:
        :param recipient_addr:
        :param balance:
        :param resource:
        :return:
        """
        Private_key = PrivateKey(bytes.fromhex(private_key))

        txn = (
            TronAPI.__client.trx.undelegate_resource(owner=sender_addr, receiver=recipient_addr, balance=balance, resource=resource)
            .build()
            .sign(Private_key)
        )
        txn.broadcast().wait()
        return txn.txid

    def transferUSDT(self,
                     private_key: str,
                     sender_addr: str,
                     recipient_addr: str,
                     amount: int,
                     FeeLimit: int):
        Private_key = PrivateKey(bytes.fromhex(private_key))
        txn = (
            TronAPI.__contract.functions.transfer(recipient_addr, amount)
            .with_owner(sender_addr)
            .fee_limit(FeeLimit)
            .build()
            .sign(Private_key)
        )
        txn.broadcast().wait()
        return txn.txid

    def visibleTransfer(self, txID: str) -> bool:
        params = {
            "value": txID,
            "visible": True
        }

        response = requests.post(f'{TronAPI.__base_url}wallet/gettransactionbyid', json=params)

        if response.status_code != 200:
            return False

        data = response.json()
        if 'ret' not in data:
            return False

        if data['ret'][0]['contractRet'] == 'SUCCESS':
            return True

        return False


    @staticmethod
    def GetAccountResource(Address: str) -> dict:
        params = {
            "address": Address,
            "visible": True
        }

        response = requests.post(f'{TronAPI.__base_url}wallet/getaccountresource', json=params)

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def GetAccount(Address: str) -> dict:
        params = {
            "address": Address,
            "visible": True
        }

        response = requests.post(f'{TronAPI.__base_url}wallet/getaccount', json=params)

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def CreateAccount(owner_address: str, account_address: str) -> dict:
        """
        只是发起一个创建请求，还未签名和广播
        :param owner_address:
        :param account_address:
        :return:
        """
        params = {
            "owner_address": owner_address,
            "account_address": account_address,
            "visible": True
        }

        response = requests.post(f'{TronAPI.__base_url}wallet/createaccount', json=params)

        if response.status_code == 200:
            return response.json()


    @staticmethod
    def BroadcastTransaction():
        pass

if __name__ == '__main__':
    pass
    # EnergyPrices = TronAPI().getEnergyPrices()
    # BandWidthPrices = TronAPI().getBandWidthPrices()
    # USDTTransferEnergyRequired = TronAPI().GetUSDTTransferEnergyRequired('TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA', '41f938be5dbfada78415575225b9ab0f10ca406abd', 10)
    # print(EnergyPrices)
    # print(BandWidthPrices)
    # print(USDTTransferEnergyRequired)

    ''' 给代理 能量'''
    # priv_key = 'ca9e7b596a4df59c45b92b5c4ec788b35fac76e05ca435fc583d6662a34b8385'
    # owner = 'TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA'
    # recipient_addr = '41f938be5dbfada78415575225b9ab0f10ca406abd'
    #
    # txid = TronAPI().DelegateResource(priv_key, owner, recipient_addr, 134000000)
    # print(txid)

    '''USDT 转账'''
    # amount = 1_000_000
    # priv_key = 'ca9e7b596a4df59c45b92b5c4ec788b35fac76e05ca435fc583d6662a34b8385'
    # owner = 'TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA'
    # recipient_addr = '41f938be5dbfada78415575225b9ab0f10ca406abd'
    # FeeLimit = TronAPI().GetFeeLimitOfUSDTTransfer(owner, recipient_addr, amount)
    # txid = TronAPI().transferUSDT(priv_key, owner, recipient_addr, amount, FeeLimit)
    # print(FeeLimit)
    # print(txid)

    # amount = 1_000_000
    # priv_key = '7f30ff2a70d90e5345ff25e102175c258441124ad43cb25c9dbd3a87d79af22b'
    # owner = 'TYgyESVzn4V7RgyRkzdmqjxwXyYA5T75xx'
    # recipient_addr = 'TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA'
    # FeeLimit = TronAPI().GetFeeLimitOfUSDTTransfer(owner, recipient_addr, amount)
    # txid = TronAPI().transferUSDT(priv_key, owner, recipient_addr, amount, FeeLimit)
    # print(FeeLimit)
    # print(txid)


    '''验证'''
    # T = TronAPI().visibleTransfer('69f30b27b066884182f70ef15ad393acac2f915884799ca670135f6b6834d2c6')
    # print(T)

    ''' 给取消代理 能量'''
    # priv_key = 'ca9e7b596a4df59c45b92b5c4ec788b35fac76e05ca435fc583d6662a34b8385'
    # owner = 'TKxYDucF7RBMM1qH6rhpFStwkMRVD5ojjA'
    # recipient_addr = '41f938be5dbfada78415575225b9ab0f10ca406abd'
    #
    # txid = TronAPI().UndelegateResource(priv_key, owner, recipient_addr, 151090000)
    # print(txid)
