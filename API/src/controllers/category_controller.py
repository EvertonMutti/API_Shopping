# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:12:57 2023

@author: Everton Castro
"""

from fastapi import APIRouter, HTTPException, Depends
from timeout_decorator import timeout, TimeoutError     
from asyncpg.exceptions import PostgresError
from src.connection.conexao import get_database_connection   
from src.schemas.schema import Categoria
from .dependences.logged_user import verifyLoggedUser


router = APIRouter()
        
@timeout(10)        
@router.delete("/delete/category/{category_id}")
async def delete_category(category_id: int, logger_user = Depends(verifyLoggedUser)):
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
@router.post("/create/category/")
async def create_category(categoria: Categoria, logger_user = Depends(verifyLoggedUser)):
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
@router.get("/select/category/{category_id}")
async def read_category(category_id: int, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM categoria WHERE categoria_id = $1"
        result = await conn.fetchrow(query, category_id)
        if result is None:
            raise HTTPException(status_code=404, detail="categoria not found")
        return Categoria(**result)

    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")

    finally:
        await conn.close()
        
        
@timeout(10)
@router.get("/select/categorys/")
async def showCategoroy(logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM categoria"
        result = await conn.fetch(query)
        if result is None:
            raise HTTPException(status_code=404, detail="categoria not found")
        categorias = [Categoria(**row) for row in result]
        return categorias

    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")

    finally:
        await conn.close()

@timeout(10)
@router.put("/select/category/{category_id}")
async def updateCategory(category_id: int,categoria: Categoria, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        
        values = (categoria.nome, category_id)

        query = "SELECT * FROM categoria WHERE categoria_id = $1" 
        # query = "UPDATE categoria SET  WHERE categoria_id = $1"
        result = await conn.fetch(query)
        if result is None:
            raise HTTPException(status_code=404, detail="categoria not found")
        else:
            query = "UPDATE categoria SET nome = ($1) WHERE categoria_id = ($2)"
            await conn.execute(query, values)
            return {"message": "Ok"}
            # EXECUTE MANY
        
        # categorias = [Categoria(**row) for row in result]
        # return categorias

    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")

    finally:
        await conn.close()