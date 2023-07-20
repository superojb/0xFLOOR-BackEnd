#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：KhalaMange.py
@Author  ：MoJeffrey
@Date    ：2023/7/18 2:22 
"""
from Tools.Khala.KhalaAPI import KhalaAPI
from Backend.settings import company_khala_address

class KhalaMange:
    __company_khala_address = company_khala_address

    @staticmethod
    def GetConfirmTransferURL(Hax: str) -> str:
        return f'https://polkaholic.io/tx/{Hax}'

    @staticmethod
    def GetCompanyAddress() -> str:
        return KhalaMange.__company_khala_address

    @staticmethod
    def GetHandlingFee() -> float:
        return 0.02

    @staticmethod
    def GenerateAddress(Identifier: str):
        """
        创建账号， 还未验证是否已经存在
        :return:
        """
        response = KhalaAPI.GenerateAddress(Identifier)
        return response['address'], response['mnemonic']

    @staticmethod
    def getBalance(address: str, Identifier: str) -> float:
        """
        给余额
        :return:
        """
        if not address:
            return 0.0
        response = KhalaAPI.getBalance(address, Identifier)
        return response['Balance']

    @staticmethod
    def Transfer(payeeAddress: str, disbursementsKey: str, num: float, Identifier: str) -> str:
        """
        交易
        :return:
        """
        response = KhalaAPI.Transfer(payeeAddress, disbursementsKey, num, Identifier)
        return response['Hex']

    @staticmethod
    def confirmTransfer(Hax: str, Identifier: str):
        """
        交易
        :return:
        """
        response = KhalaAPI.confirmTransfer(Hax, Identifier)
        if 'error' in response:
            return False, response['error']

        if 'status' in response:
            if response['status'] == 'finalized':
                return True, ''
            else:
                return False, ''

    @staticmethod
    def GetPhalaComputationSessions(minerAccount: str, Identifier: str):
        response = KhalaAPI.getPhalaComputation_sessions(minerAccount, Identifier)
        return response

    @staticmethod
    def GetPhalaComputationRevenue(response):
        return response['totalReward']

    @staticmethod
    def getPhalaComputationIsWork(response) -> bool:
        if response['state'] == 'WorkerIdle':
            return True

        return False
