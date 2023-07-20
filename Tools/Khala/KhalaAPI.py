#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：KhalaMange.py
@Author  ：MoJeffrey
@Date    ：2023/7/18 2:22 
"""
import json

import requests
from loguru import logger

from Backend.settings import Khala_URL, PolkaholicAPI_URL
from Tools.Khala.Exception.KhalaAPIRequestError import KhalaAPIRequestError


class KhalaAPI:
    __base_url = Khala_URL
    __PolkaholicAPI_url = PolkaholicAPI_URL

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
        }

        if params:
            kwargs['json'] = params

        ReTry = 0
        MaxReTry = 5

        while True:
            try:
                response = requests.post(**kwargs) if Post else requests.get(**kwargs)
                break
            except requests.exceptions.ConnectionError:
                if ReTry >= MaxReTry:
                    raise Exception('無法連接KhalaAPI')
                logger.info("requests.exceptions.ConnectionError Retry")
                ReTry += 1
                continue

        if response.status_code == 200:
            responseData = json.loads(response.text)
            KhalaAPI.Log(URL, Identifier, params, responseData, 1)
            return responseData

        raise KhalaAPIRequestError(URL, params, Identifier)

    @staticmethod
    def Log(URL: str, Identifier: str, params: dict, response: dict, type: int):
        if type == 1:
            logger.info(f"URL: {URL}; Identifier: {Identifier}; params: {params}; response: {response}")
        elif type == 2:
            logger.error(f"URL: {URL}; Identifier: {Identifier}; params: {params}; response: {response}")

    @staticmethod
    def GenerateAddress(Identifier: str):
        """
        创建账号
        :return:
        """
        response = KhalaAPI.Requests(URL=f'{KhalaAPI.__base_url}api/create_address', params={}, Identifier=Identifier)
        return response

    @staticmethod
    def getBalance(address: str, Identifier: str):
        """
        给余额
        :return:
        """
        params = {
            "address": address,
        }

        response = KhalaAPI.Requests(URL=f'{KhalaAPI.__base_url}api/get_balance', params=params, Identifier=Identifier)
        return response

    @staticmethod
    def Transfer(payeeAddress: str, disbursementsKey: str, num: float, Identifier: str):
        """
        交易
        :return:
        """
        params = {
            "payeeAddress": payeeAddress,
            "disbursementsKey": disbursementsKey,
            "num": num,
        }

        response = KhalaAPI.Requests(URL=f'{KhalaAPI.__base_url}api/transfer', params=params, Identifier=Identifier)
        return response

    @staticmethod
    def confirmTransfer(Hax: str, Identifier: str):
        """
        確認交易
        :return:
        """
        response = KhalaAPI.Requests(URL=f'{KhalaAPI.__PolkaholicAPI_url}tx/{Hax}', params={}, Identifier=Identifier, Post=False)
        return response

    @staticmethod
    def getPhalaComputation_sessions(minerAccount: str, Identifier: str):
        params = {
            "AccountId32": minerAccount,
        }

        response = KhalaAPI.Requests(URL=f'{KhalaAPI.__base_url}api/getPhalaComputation_sessions', params=params, Identifier=Identifier)
        return response