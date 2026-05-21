from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/minicursos/{minicurso_id}/avaliacoes")
def listar_avaliacoes(minicurso_id: int, db: Session = Depends(get_db)):
    avaliacoes = db.query(models.Avaliacao).filter(
        models.Avaliacao.minicurso_id == minicurso_id
    ).all()

    return avaliacoes