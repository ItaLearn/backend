from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.delete("/minicursos/{minicurso_id}")
def deletar_minicurso(minicurso_id: int, db: Session = Depends(get_db)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()
    
    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado!")
        
    db.delete(minicurso)
    db.commit()
    
    return {"mensagem": "Minicurso removido com sucesso!"}