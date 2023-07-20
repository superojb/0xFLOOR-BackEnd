#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：TronAPIRequestError.py
@Author  ：MoJeffrey
@Date    ：2023/5/11 18:24 
"""
class KhalaAPIRequestError(Exception):
    __Msg = None

    def __init__(self, url: str, params: dict, Identifier: str):
        super().__init__(self)
        self.__Msg = f'URL: {url}; Params: {params}; Identifier: {Identifier}'

    def __str__(self):
        Msg = "Khala api request error"
        return f"{Msg}: {self.__Msg}"
