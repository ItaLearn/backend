from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/aulas/{aula_id}/comentarios")
def listar_comentarios(aula_id: int, db: Session = Depends(get_db)):
    comentarios = db.query(models.ComentarioAula).filter(models.ComentarioAula.aula_id == aula_id).all()

    return comentarios