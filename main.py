from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma de Estudos API")

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

class AtualizarMinicurso(BaseModel):
    titulo: str
    descricao: str


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

@app.post("/login")
def login(dados: FazerLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    
    if not usuario or usuario.senha != dados.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
        
    return {"mensagem": "Login aprovado", "usuario": usuario.nome_usuario}

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

@app.put("/minicursos/{minicurso_id}")
def atualizar_minicurso(minicurso_id: int, dados: AtualizarMinicurso, db: Session = Depends(get_db)):
    minicurso_db = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()
    
    if not minicurso_db:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")
    
    minicurso_db.titulo = dados.titulo
    minicurso_db.descricao = dados.descricao
    
    db.commit()
    db.refresh(minicurso_db)
    return {"mensagem": "Minicurso atualizado com sucesso!", "curso": minicurso_db}

@app.delete("/minicursos/{minicurso_id}")
def apagar_minicurso(minicurso_id: int, db: Session = Depends(get_db)):
    minicurso_db = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()
    
    if not minicurso_db:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")
    
    db.delete(minicurso_db)
    db.commit()
    return {"mensagem": "Minicurso removido com sucesso!"}