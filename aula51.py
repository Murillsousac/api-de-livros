from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = "sqlite:///./Livros.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI(
    title="API de Tarefas",
    description="API para gerenciar tarefas",
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

class livroDB(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True,index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer)

class livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int


def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, meu_usuario)
    is_password_correct = secrets.compare_digest(credentials.password, minha_senha)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401, detail="usuario ou senha incorreto!!", headers={"WWW-Authenticate": "Basic"})

@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario),):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit são invalidos")
    
    livros = db.query(livroDB).offset((page-1) * limit).limit(limit).all()


    if not livros:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado!!")

    total_livros = db.query(livroDB).count()


    return{
        "page": page,
        "limit": limit,
        "total": total_livros,
        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro": livro.autor_livro, "ano_livro": livro.ano_livro }for livro in livros] 
    }





@app.post("/adiciona")
def post_livros(livro: livro, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(livroDB).filter(livroDB.nome_livro == livro.nome_livro, livroDB.autor_livro == livro.autor_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="esse livro já existe dentro do banco de dados!!!")
    
    novo_livro = livroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    return{"message": "O livro foi criado com sucesso"}

@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: livro, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(livroDB).filter(livroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="esse livro não existe dentro do banco de dados!!!")

    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro

    db.commit()
    db.refresh(db_livro)

    return {"message": "Seu livro foi atualizado com sucesso"}

@app.delete("/deleta/{id_livro}")
def delete_livro(id_livro : int, db: Session = Depends(sessao_db),credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(livroDB).filter(livroDB.id == id_livro).first()
    
    if not db_livro:
        raise HTTPException(status_code=404, detail="esse livro não existe dentro do banco de dados!!!")
    
    db.delete(db_livro)
    db.commit()

    return {"message": "Seu livro foi deletado com sucesso"}