from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/cursos/filtrar")
def filtrar_cursos(categoria_id: int, db: Session = Depends(get_db)):
    cursos = db.query(models.Minicurso).join(models.Minicurso.categorias).filter(models.Categoria.id == categoria_id).all()

    return cursos