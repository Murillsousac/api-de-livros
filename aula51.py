from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os 

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catálogo de livros",
    version="1.0.0",
    contact={
        "name": "Murillo Sousa",
        "email": "sousamurillo4655@gmail.com"   
    }
)

meu_usuario = "admin"
minha_senha = "admin"

security = HTTPBasic()

meus_livros = {

}

class livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, meu_usuario)
    is_password_correct = secrets.compare_digest(credentials.password, minha_senha)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401, detail="usuario ou senha incorreto!!", headers={"WWW-Authenticate": "Basic"})

@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit são invalidos")
    
    if not meus_livros:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado!!")

    livros_ordenados = sorted(meus_livros.items(), key=lambda x: x[0])
    
    start = (page - 1) * limit
    end = start + limit

    

    livros_paginados = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"],"autor_livro":livro_data["autor_livro"],"ano_livro": livro_data["ano_livro"]}
        for id_livro, livro_data in livros_ordenados[start:end] 
    ]

    return{
        "page": page,
        "limit": limit,
        "total": len(meus_livros),
        "livros": livros_paginados
    }



@app.post("/adiciona")
def post_livros(id_livro: int, livro: livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="esse livro já existe, meu parceiro")
    else:
        meus_livros[id_livro] = livro.dict() 
        return {"message": "O livro foi criado com sucesso"}

@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: livro,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=400, detail="esse livro não foi encontrado")
    else:
        meus_livros[id_livro] = livro.dict() 

        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}

@app.delete("/deleta/{id_livro}")
def delete_livro(id_livro : int,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=400, detail="Esse livro nao foi encontrado")
    else:
        del meus_livros[id_livro]

        return {"message": "Seu livro foi deletado com sucesso"}