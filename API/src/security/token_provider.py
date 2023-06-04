# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 00:37:53 2023

@author: Everton
"""
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "ImsexyandIknowit"
ALGORITHM = 'HS256'
EXPIRES_IN_MIN = 3 * 10000

def createAcessToken(data: dict):
    data_copy = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes = EXPIRES_IN_MIN)
    data_copy.update({'exp': expiration})
    token_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    
    return token_jwt

def verifyAcessToken(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM] )
    return payload.get('sub')