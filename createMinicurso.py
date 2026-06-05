from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CriarMinicurso
import models

router = APIRouter()

@router.post("/usuarios/{autor_id}/minicursos")
def criar_minicurso(autor_id: int, minicurso: CriarMinicurso, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).filter(models.Categoria.id.in_(minicurso.categorias)).all()
    novo_minicurso = models.Minicurso(autor_id=autor_id, titulo=minicurso.titulo, descricao=minicurso.descricao, categorias=categorias)
    
    db.add(novo_minicurso)
    db.commit()
    db.refresh(novo_minicurso)
    
    return {"mensagem": "Minicurso criado com sucesso!", "id_minicurso": novo_minicurso.id}