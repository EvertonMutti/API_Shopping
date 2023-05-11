# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:20:45 2023

@author: Everton Castro
"""

from pydantic import BaseModel

class Logs(BaseModel):
    data_hora: str
    users_user_fk: int
    descricao: str