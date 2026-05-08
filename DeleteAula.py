from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.delete("/{id_aula}")
def deletar_aula(id_aula: int, db: Session = Depends(get_db)):
    aula = db.query(models.Aula).filter(models.Aula.id == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    
    db.delete(aula)
    db.commit()
    return "Aula deletada"