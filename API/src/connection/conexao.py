# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 10:17:24 2023

@author: Everton
"""
import asyncpg


async def get_database_connection():
    conn = await asyncpg.connect(user='ivcevgvt',
                                 password='SXsn6iGF_s4ftrU2_ogFdPln3Ogpqgkd',
                                 database='ivcevgvt',
                                 host='motty.db.elephantsql.com')
    return conn
