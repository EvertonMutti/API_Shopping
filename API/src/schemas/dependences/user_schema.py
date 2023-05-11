# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 00:22:57 2023

@author: Everton
"""

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: Optional[int] = None
    name : str 
    email : str 
    password : str 
    empresa_fk: int
    
    
class Login(BaseModel):
    email: str 
    password: str
    