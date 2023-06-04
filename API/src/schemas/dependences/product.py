# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:19:14 2023

@author: Everton Castro
"""
from typing import Optional
from pydantic import BaseModel

class Produto(BaseModel):
    produtos_id : int
    nome: str
    preco: float
    descricao: str
    codigo: str
    is_Published: Optional[bool] = False
    categoria_categoria_fk: int
    
class SimpleProduto(BaseModel):
    produtos_id: str
    nome: str