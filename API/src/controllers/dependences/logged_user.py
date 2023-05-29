# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 17:13:26 2023

@author: Everton
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from src.connection.conexao import get_database_connection 
from src.security.token_provider import verifyAcessToken


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/User/login")


async def verifyLoggedUser(token: str = Depends(oauth2_schema)):
    conn = None
    try:
        
        payload = verifyAcessToken(token)
    
        conn = await get_database_connection()
        
        query_verify_user = "SELECT email, empresa_empresa_fk  FROM users WHERE email = $1"
        user = await conn.fetchrow(query_verify_user, payload)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except jwt.JWTError:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    finally:
        if conn:
            await conn.close()
