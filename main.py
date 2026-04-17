from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma de Estudos API")

class CriarUsuario(BaseModel):
    nome: str
    email: str
    senha: str

class FazerLogin(BaseModel):
    email: str
    senha: str

class CriarMinicurso(BaseModel):
    titulo: str
    descricao: str
    autor_email: str


@app.post("/usuarios")
def criar_usuario(usuario: CriarUsuario, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    novo_usuario = models.Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) 
    
    return {"mensagem": f"Usuário {novo_usuario.nome} criado com sucesso!", "id": novo_usuario.id}

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