# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:12:57 2023

@author: Everton Castro
"""

from fastapi import APIRouter, HTTPException
from timeout_decorator import timeout, TimeoutError     
from asyncpg.exceptions import PostgresError
from src.connection.conexao import get_database_connection   
from src.schemas.schema import Categoria


router = APIRouter()
        
@timeout(10)        
@router.delete("/delete/category/{category_id}")
async def delete_category(category_id: int):
    conn = None
    try:
        conn = await get_database_connection()
        query = "DELETE FROM categoria WHERE categoria_id = $1"
        result = await conn.execute(query, category_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="category not found")
        return {"message": "category deleted"}
    
    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")
        
    finally:
        await conn.close()
        
@timeout(10)
@router.post("/create/categoria/")
async def create_product(categoria: Categoria):
    conn = None
    try:
        conn = await get_database_connection()

        values = (categoria.nome)

        query = "INSERT INTO categoria (nome) VALUES ($1)"
        await conn.execute(query, values)
        return {"message": "Ok"}

    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")

    finally:
        await conn.close()
        
@timeout(10)
@router.get("/select/categoria/{categoria_id}")
async def read_categoria(categoria_id: int):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM categoria WHERE categoria_id = $1"
        result = await conn.fetchrow(query, categoria_id)
        if result is None:
            raise HTTPException(status_code=404, detail="categoria not found")
        return Categoria(**result)

    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")

    finally:
        await conn.close()