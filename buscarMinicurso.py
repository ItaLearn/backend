from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/minicursos/buscar")
def buscar_minicursos(nome: str, db: Session = Depends(get_db)):

    minicursos = db.query(models.Minicurso).filter(models.Minicurso.titulo.ilike(f"%{nome}%")).all()

    if not minicursos:
        return {"mensagem": "Nenhum minicurso encontrado"}

    return minicursos