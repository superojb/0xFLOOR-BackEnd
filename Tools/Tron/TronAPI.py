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
from Backend.settings import Tron_URL, usdt_contract_address
from Tools.Tron.Exception.TronAPIRequestError import TronAPIRequestError

class TronAPI:
    __usdt_contract_address = usdt_contract_address
    __base_url = Tron_URL
    __client = None

    def __init__(self, tron: Tron):
        TronAPI.__client = tron

    @staticmethod
    def Requests(URL: str, params: dict, Identifier: str, Post: bool = True) -> dict:
        """
        :param URL:
        :param params:
        :param Type:
        :param Identifier: 识别码。为了追踪日志
        :return:
        """
        response = None
        kwargs = {
            "url": URL,
            "json": params,
        }
        while True:
            try:
                response = requests.post(**kwargs) if Post else requests.get(**kwargs)
                break
            except requests.exceptions.ConnectionError:
                logger.info("requests.exceptions.ConnectionError Retry")
                continue
        if response.status_code == 200:
            responseData = response.json()
            TronAPI.Log(URL, Identifier, params, responseData, 1)
            return responseData

        raise TronAPIRequestError(URL, params, Identifier)

    @staticmethod
    def Log(URL: str, Identifier: str, params: dict, response: dict, type: int):
        if type == 1:
            logger.info(f"URL: {URL}; Identifier: {Identifier}; params: {params}; response: {response}")
        elif type == 2:
            logger.error(f"URL: {URL}; Identifier: {Identifier}; params: {params}; response: {response}")

    @staticmethod
    def getEnergyPrices() -> int:
        response = requests.get(f'{TronAPI.__base_url}wallet/getenergyprices')
        if response.status_code == 200:
            data = response.json()
            return int(data['prices'].split(',')[-1].split(':')[1])

    @staticmethod
    def getBandWidthPrices() -> int:
        response = requests.get(f'{TronAPI.__base_url}wallet/getbandwidthprices')
        if response.status_code == 200:
            data = response.json()
            return int(data['prices'].split(',')[-1].split(':')[1])

    @staticmethod
    def GetUSDTTransferEnergyRequired(Identifier, sender_addr: str, recipient_addr: str, amount: int) -> int:
        raw = trx_abi.encode_single("(address,uint256)", [recipient_addr, amount])
        params = {
            "owner_address": sender_addr,
            "contract_address": TronAPI.__usdt_contract_address,
            "function_selector": "transfer(address,uint256)",
            "parameter": raw.hex(),
            "visible": True
        }
        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/triggerconstantcontract',
                                    params=params, Identifier=Identifier)
        return int(response['energy_used'])

    @staticmethod
    def DelegateResource(Identifier: str,
                         sender_addr: str,
                         recipient_addr: str,
                         balance: int,
                         resource: str) -> dict:
        """
        把能量代理过去
        :param sender_addr:
        :param recipient_addr:
        :param balance:
        :param resource:
        :return:
        """
        params = {
            "owner_address": sender_addr,
            "receiver_address": recipient_addr,
            "balance": balance,
            "resource": resource,
            "lock": False,
            "visible": True
        }
        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/delegateresource', params=params,
                                    Identifier=Identifier)
        return response

    @staticmethod
    def GetDelegatedResourceV2(Identifier: str, fromAddress: str, toAddress: str) -> dict:
        params = {
            "fromAddress": fromAddress,
            "toAddress": toAddress,
            "visible": True
        }
        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/getdelegatedresourcev2', params=params,
                                    Identifier=Identifier)
        return response

    @staticmethod
    def UnDelegateResource(Identifier: str,
                           sender_addr: str,
                           recipient_addr: str,
                           balance: int,
                           resource: str) -> dict:
        """
        取消能量代理过去
        :param private_key:
        :param sender_addr:
        :param recipient_addr:
        :param balance:
        :param resource:
        :return:
        """
        params = {
            "owner_address": sender_addr,
            "receiver_address": recipient_addr,
            "balance": balance,
            "resource": resource,
            "visible": True
        }
        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/undelegateresource', params=params,
                                    Identifier=Identifier)
        return response

    @staticmethod
    def TriggerSmartContract(Identifier: str,
                             contract_address: str,
                             sender_addr: str,
                             recipient_addr: str,
                             amount: int,
                             FeeLimit: int):
        raw = trx_abi.encode_single("(address,uint256)", [recipient_addr, amount])
        params = {
            "owner_address": sender_addr,
            "contract_address": contract_address,
            "function_selector": "transfer(address,uint256)",
            "parameter": raw.hex(),
            "visible": True,
            "fee_limit": FeeLimit
        }
        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/triggersmartcontract',
                                    params=params, Identifier=Identifier)

        return response

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
    def GetAccountResource(Identifier, Address: str) -> dict:
        params = {
            "address": Address,
            "visible": True
        }

        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/getaccountresource', params=params,
                                    Identifier=Identifier)
        return response


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
    def CreateAccount(Identifier: str, owner_address: str, account_address: str) -> dict:
        """
        只是发起一个创建请求，还未签名和广播
        :param Identifier:
        :param owner_address:
        :param account_address:
        :return:
        """
        params = {
            "owner_address": owner_address,
            "account_address": account_address,
            "visible": True
        }

        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/createaccount', params=params, Identifier=Identifier)
        return response


    @staticmethod
    def BroadcastTransaction(Identifier, transactionInfo: dict):
        """
        广播交易
        :param Identifier:
        :param transactionInfo:
        :return:
        """
        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}wallet/broadcasttransaction',
                                    params=transactionInfo, Identifier=Identifier)
        return response

    @staticmethod
    def QueryTransaction(Identifier, TransactionId: str) -> dict:
        params = {
            "value": TransactionId,
            "visible": True
        }

        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}walletsolidity/gettransactionbyid',
                                    params=params, Identifier=Identifier)
        return response

    @staticmethod
    def getTransactionInfoById(Identifier, TransactionId: str):
        params = {
            "value": TransactionId,
        }

        response = TronAPI.Requests(URL=f'{TronAPI.__base_url}walletsolidity/gettransactioninfobyid',
                                    params=params, Identifier=Identifier)
        return response

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
