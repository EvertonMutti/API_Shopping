# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:02:05 2023

@author: Everton Castro
"""

from fastapi import APIRouter
from src.controllers import user_controller, product_controller, company_controller, category_controller

router = APIRouter()

#Router products
router.include_router(product_controller.router, prefix="/products", tags=['Products'])
#Router authentication and authorization
router.include_router(user_controller.router, prefix="/User", tags=['Users'])
#Router products
router.include_router(company_controller.router, prefix="/Company", tags=['Company'])
#Router authentication and authorization
router.include_router(category_controller.router, prefix="/Category", tags=['Category'])