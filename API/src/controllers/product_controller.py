# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:08:47 2023

@author: Everton Castro
"""
from fastapi import APIRouter, HTTPException, Depends
from timeout_decorator import timeout, TimeoutError     
from asyncpg.exceptions import PostgresError
from src.connection.conexao import get_database_connection   
from src.schemas.schema import Produto
from .dependences.logged_user import verifyLoggedUser

router = APIRouter()
        
@timeout(10)        
@router.delete("/delete/product/{product_id}")
async def delete_product(product_id: int, logger_user: str = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        empresa_id = logger_user['empresa_empresa_fk']
        query = "DELETE FROM produto WHERE produtos_id  = $1 and empresa_empresa_fk = $2"
        result = await conn.execute(query, product_id, empresa_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted"}
    
    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")
        
    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")
        
    finally:
        await conn.close()
        
@timeout(10)
@router.post("/create/product/")
async def create_product(produto: Produto, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        empresa_id = logger_user['empresa_empresa_fk']

        values = (produto.nome, produto.preco,
                  produto.descricao, produto.codigo,
                  produto.is_Published, produto.categoria_categoria_fk)

        ver_emp = "SELECT empresa_id FROM empresa WHERE empresa_id = $1"

        ver_cat = "SELECT categoria_id FROM categoria WHERE categoria_id = $1"

        empresa = await conn.fetchrow(ver_emp, empresa_id)
        categoria = await conn.fetchrow(ver_cat, produto.categoria_categoria_fk)

        # return{ "message": values, "comando_1": empresa, "comando_2": categoria }

        if empresa is None:
            raise HTTPException(status_code=404, detail="empresa not found")
        elif categoria is None:
             raise HTTPException(status_code=404, detail="categoria not found")

        query = "INSERT INTO produto (nome, preco, descricao, codigo, is_published, categoria_categoria_fk, empresa_empresa_fk ) VALUES ($1, $2, $3, $4, $5, $6, $7)"
        await conn.execute(query, *values, empresa_id)
        return {"message": "Produto inserido com sucesso"}

    except PostgresError as e:
        return HTTPException(status_code=409 , detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408 , detail=f"Error {e}")

    except HTTPException as e:
        return HTTPException(status_code=404, detail=f"Error {e}")
    
    finally:
        await conn.close()

@timeout(10)
@router.get("/select/product/{product_id}")
async def read_produto(product_id: int, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        
        empresa_id = logger_user['empresa_empresa_fk']
        query = "SELECT * FROM produto WHERE produtos_id = $1 and empresa_empresa_fk = $2"
        result = await conn.fetchrow(query, product_id, empresa_id)
        
        if result is None:
            raise HTTPException(status_code=404, detail=f"produto not found{empresa_id}")
        return Produto(**result)

    except PostgresError as e:
        return HTTPException(status_code=409, detail=f"Error {e}")

    except TimeoutError as e:
        return HTTPException(status_code=408, detail=f"Error {e}")

    finally:
        await conn.close()