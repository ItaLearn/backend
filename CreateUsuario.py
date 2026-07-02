from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CriarUsuario
from auth import gerar_hash_senha
import models

router = APIRouter()

@router.post("/usuarios")
def criar_usuario(usuario: CriarUsuario, db: Session = Depends(get_db)):
    email_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado!")
        
    user_existente = db.query(models.Usuario).filter(models.Usuario.nome_usuario == usuario.nome_usuario).first()
    if user_existente:
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso!")
    
    senha_hash = gerar_hash_senha(usuario.senha)
    
    novo_usuario = models.Usuario(
        nome=usuario.nome, 
        nome_usuario=usuario.nome_usuario,
        email=usuario.email, 
        senha=senha_hash,
        profissao=usuario.profissao
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) 
    
    return {"mensagem": f"Usuário {novo_usuario.nome_usuario} criado com sucesso!", "id": novo_usuario.id}