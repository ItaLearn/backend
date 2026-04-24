from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import engine, get_db


from CreateAula import router as aula_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma de Estudos API")

app.include_router(aula_router)

class CriarUsuario(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    nome_usuario: str = Field(min_length=3, max_length=15)
    email: str
    senha: str
    profissao: str

class FazerLogin(BaseModel):
    email: str
    senha: str

class CriarMinicurso(BaseModel):
    titulo: str
    descricao: str
    autor_email: str

class CriarAula(BaseModel):
    id_minicurso: int
    titulo: str
    conteudo: str
    ordem: int

@app.post("/usuarios")
def criar_usuario(usuario: CriarUsuario, db: Session = Depends(get_db)):
    email_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado!")
        
    user_existente = db.query(models.Usuario).filter(models.Usuario.nome_usuario == usuario.nome_usuario).first()
    if user_existente:
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso!")
    
    novo_usuario = models.Usuario(
        nome=usuario.nome, 
        nome_usuario=usuario.nome_usuario,
        email=usuario.email, 
        senha=usuario.senha,
        profissao=usuario.profissao
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) 
    
    return {"mensagem": f"Usuário {novo_usuario.nome_usuario} criado com sucesso!", "id": novo_usuario.id}

@app.post("/minicursos")
def criar_minicurso(minicurso: CriarMinicurso, db: Session = Depends(get_db)):
    novo_minicurso = models.Minicurso(titulo=minicurso.titulo, descricao=minicurso.descricao, autor_email=minicurso.autor_email)
    
    db.add(novo_minicurso)
    db.commit()
    db.refresh(novo_minicurso)
    
    return {"mensagem": "Minicurso criado com sucesso!", "id_minicurso": novo_minicurso.id}

@app.get("/minicursos")
def listar_minicursos(db: Session = Depends(get_db)):
    minicursos = db.query(models.Minicurso).all()
    return {"minicursos_disponiveis": minicursos}