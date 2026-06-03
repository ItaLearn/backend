from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import AtualizarMinicurso
import models

router = APIRouter()

@router.put("/minicursos/{minicurso_id}")
def atualizar_minicurso(minicurso_id: int, minicurso_atualizado: AtualizarMinicurso, db: Session = Depends(get_db)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()
    
    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado!")

    if minicurso_atualizado.titulo:
        minicurso.titulo = minicurso_atualizado.titulo
    if minicurso_atualizado.descricao:
        minicurso.descricao = minicurso_atualizado.descricao
        
    db.commit()
    db.refresh(minicurso)
    
    return {"mensagem": "Minicurso atualizado com sucesso!"}