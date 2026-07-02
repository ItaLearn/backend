from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.get("/minicursos/{minicurso_id}/likes")
def contar_likes(minicurso_id: int, db: Session = Depends(get_db)):
    total_likes = db.query(models.LikeCurso).filter(models.LikeCurso.minicurso_id == minicurso_id).count()

    return {
        "minicurso_id": minicurso_id,
        "total_likes": total_likes
    }