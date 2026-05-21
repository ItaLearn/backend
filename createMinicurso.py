from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CriarMinicurso
import models

router = APIRouter()

@router.post("/minicursos")
def criar_minicurso(minicurso: CriarMinicurso, db: Session = Depends(get_db)):
    novo_minicurso = models.Minicurso(titulo=minicurso.titulo, descricao=minicurso.descricao, autor_email=minicurso.autor_email)
    
    db.add(novo_minicurso)
    db.commit()
    db.refresh(novo_minicurso)
    
    return {"mensagem": "Minicurso criado com sucesso!", "id_minicurso": novo_minicurso.id}