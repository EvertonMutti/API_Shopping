# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:19:36 2023

@author: Everton Castro
"""
from pydantic import BaseModel

class Categoria(BaseModel):
    nome: str