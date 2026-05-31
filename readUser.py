from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "nome_usuario": usuario.nome_usuario,
        "email": usuario.email,
        "profissao": usuario.profissao
    }