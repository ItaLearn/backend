from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/minicursos")
def listar_minicursos(db: Session = Depends(get_db)):
    minicursos = db.query(models.Minicurso).all()
    return {"minicursos_disponiveis": minicursos}

@router.get("/minicursos/{minicurso_id}")
def obter_minicurso(minicurso_id: int, db: Session = Depends(get_db)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()
    
    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado!")
        
    return {
        "id": minicurso.id,
        "titulo": minicurso.titulo,
        "descricao": minicurso.descricao,
        "autor_email": minicurso.autor_email,
        "aulas": minicurso.aulas
    }