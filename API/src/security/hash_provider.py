# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 00:16:11 2023

@author: Everton
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"])

def verifyPassword(text: str, hash) -> bool:
    return pwd_context.verify(text, hash)

def getPasswordHash(password: str) -> str:
    return pwd_context.hash(password)

