from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

meus_livros = {

}

@app.get("/livros")
def get_livros():
    if not meus_livros:
        return{"message": "nao existe nenhum livro!"}
    else:
        return{"livros": meus_livros}
    
@app.post("/adiciona")
def post_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="esse livro já existe, meu parceiro")
    else:
        meus_livros[id_livro] = {"nome_livro": nome_livro, "autor_livro": autor_livro, "ano_livro": ano_livro }
        return {"message": "O livro foi criado com sucesso"}

@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=400, detail="esse livro não foi encontrado")
    else:
        if nome_livro:
            meu_livro["nome_livro"] = nome_livro
        if autor_livro:
            meu_livro["autor_livro"] = autor_livro
        if ano_livro:
            meu_livro["ano_livro"] = ano_livro 

        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}

@app.delete("/deleta/{id_livro}")
def delete_livro(id_livro : int):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=400, detail="Esse livro nao foi encontrado")
    else:
        del meus_livros[id_livro]

        return {"message": "Seu livro foi deletado com sucesso"}