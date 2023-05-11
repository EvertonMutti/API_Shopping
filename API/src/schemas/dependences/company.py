# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:19:29 2023

@author: Everton Castro
"""
from pydantic import BaseModel

class Empresa(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: str
    email: str    
