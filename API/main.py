# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 19:26:24 2023

@author: Everton
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router

app = FastAPI()

origins = ["http://localhost",
           "http://localhost:8080",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
                
