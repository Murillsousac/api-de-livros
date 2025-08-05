from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

meus_livros = {

}

class livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

@app.get("/livros")
def get_livros():
    if not meus_livros:
        return{"message": "nao existe nenhum livro!"}
    else:
        return{"livros": meus_livros}
    
@app.post("/adiciona")
def post_livros(id_livro: int, livro: livro):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="esse livro já existe, meu parceiro")
    else:
        meus_livros[id_livro] = livro.dict() 
        return {"message": "O livro foi criado com sucesso"}

@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: livro):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=400, detail="esse livro não foi encontrado")
    else:
        meus_livros[id_livro] = livro.dict() 

        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}

@app.delete("/deleta/{id_livro}")
def delete_livro(id_livro : int):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=400, detail="Esse livro nao foi encontrado")
    else:
        del meus_livros[id_livro]

        return {"message": "Seu livro foi deletado com sucesso"}