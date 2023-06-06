# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:11:38 2023

@author: Everton Castro
"""

from fastapi import APIRouter, HTTPException, Depends
from timeout_decorator import timeout, TimeoutError     
from asyncpg.exceptions import PostgresError
from src.connection.conexao import get_database_connection   
from src.schemas.schema import Empresa
from .dependences.logged_user import verifyLoggedUser


router = APIRouter()
        
@timeout(10)        
@router.delete("/delete/empresa/{empresa_id}")
async def delete_empresa(empresa_id: int, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        query = "DELETE FROM empresa WHERE empresa_id = $1"
        result = await conn.execute(query, empresa_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="empresa not found")
        return {"message": "empresa deleted"}
    
    except PostgresError as e:
        return {"message": f"Error {e}"}
        
    except TimeoutError as e:
        return {"message": f"Error {e}"}
        
    finally:
        await conn.close()

"""        
@timeout(10)
@router.post("/create/company/")
async def create_empresa(empresa: Empresa, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()

        values = (empresa.nome_fantasia, empresa.razao_social,
                  empresa.email, empresa.cnpj)

        query = "INSERT INTO empresa (nome_fantasia, razao_social, email, cnpj) VALUES ($1, $2, $3, $4)"
        await conn.execute(query, *values)
        return {"message": "Empresa criada com sucesso!"}

    except PostgresError as e:
        return {"message": f"Error {e}"}

    except TimeoutError as e:
        return {"message": f"Error {e}"}

    except HTTPException as e:
        return {"message": f"Error {e}"}

    finally:
        await conn.close()

"""


@timeout(10)
@router.get("/select/empresa/")
async def read_empresa(logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        empresa_id = logger_user['empresa_empresa_fk']
        conn = await get_database_connection()
        query = "SELECT * FROM empresa WHERE empresa_id = $1"
        result = await conn.fetchrow(query, empresa_id)
        if result is None:
            raise HTTPException(status_code=404, detail="empresa not found")
        return Empresa(**result)

    except PostgresError as e:
        return {"message": f"Error {e}"}

    except TimeoutError as e:
        return {"message": f"Error {e}"}

    finally:
        await conn.close()

@timeout(10)
@router.put("/update/empresa/{empresa_cnpj}")
async def updateEmpresa(empresa_cnpj: str, empresa: Empresa, logger_user = Depends(verifyLoggedUser)):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT cnpj FROM empresa WHERE cnpj = $1"
        
        values = (empresa.nome_fantasia, empresa.razao_social,
                  empresa.email, empresa.cnpj, empresa_cnpj)
        
        result = await conn.fetchrow(query, empresa_cnpj)
        if result is None:
            raise HTTPException(status_cod=400, detail="Empresa not found")
        else:
            if values:
                query = "UPDATE empresa SET nome_fantasia = $1, razao_social = $2, email = $3, cnpj = $4 WHERE cnpj = $5"
                await conn.execute(query, *values)
                return { "message" : "Ok" }

    except PostgresError as e:
        return {"message": f"Error {e}"}

    except TimeoutError as e:
        return {"message": f"Error {e}"}

    finally:
        await conn.close()