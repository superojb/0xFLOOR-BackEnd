#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：Mysql.py
@Author  ：MoJeffrey
@Date    ：2023/5/2 21:23 
"""

class Mysql:

    @staticmethod
    def dictFetchAll(cursor):
        desc = cursor.description

        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]