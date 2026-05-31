from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        
    db.delete(usuario)
    db.commit()
    
    return {"mensagem": "Usuário removido com sucesso!"}