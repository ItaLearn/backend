from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import AtualizarUsuario 
import models

router = APIRouter()

@router.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario_atualizado: AtualizarUsuario, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    
    usuario.nome = usuario_atualizado.nome
    usuario.profissao = usuario_atualizado.profissao
    
    if usuario_atualizado.senha:
        usuario.senha = usuario_atualizado.senha
        
    db.commit()
    db.refresh(usuario)
    
    return {"mensagem": f"Usuário {usuario.nome_usuario} atualizado com sucesso!"}