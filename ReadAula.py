from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/minicurso/{id_minicurso}")
def listar_aulas(id_minicurso: int, db: Session = Depends(get_db)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == id_minicurso).first()
    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")

    aulas = db.query(models.Aula).filter(models.Aula.id_minicurso == id_minicurso).order_by(models.Aula.ordem.asc()).all()
    if not aulas:
        raise HTTPException(status_code=404, detail="Sem aulas")
    return aulas


@router.get("/{id_aula}")
def buscar_aula(id_aula: int, db: Session = Depends(get_db)):
    aula = db.query(models.Aula).filter(models.Aula.id == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    return aula