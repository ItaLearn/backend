from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/minicursos/buscar")
def buscar_minicursos(nome: str = None, autor: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Minicurso).join(models.Usuario)
    
    if nome:
        query = query.filter(models.Minicurso.titulo.ilike(f"%{nome}%"))
    if autor:
        query = query.filter(models.Usuario.nome_usuario.ilike(f"%{autor}%"))
    minicursos = query.all()
    if not minicursos:
        return {"mensagem": "Nenhum minicurso encontrado"}

    return minicursos