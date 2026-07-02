from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.get("/minicursos/{minicurso_id}/progresso")
def progresso(minicurso_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    total_aulas = db.query(models.Aula).filter(models.Aula.id_minicurso == minicurso_id).count()

    if total_aulas == 0:
        return {
            "minicurso_id": minicurso_id,
            "total_aulas": 0,
            "aulas_concluidas": 0,
            "progresso": 0
        }

    aulas_concluidas = db.query(models.ProgressoAula).filter(
        models.ProgressoAula.usuario_id == usuario_logado.id,
        models.ProgressoAula.minicurso_id == minicurso_id,
        models.ProgressoAula.concluida == True
    ).count()

    progresso = (aulas_concluidas / total_aulas) * 100

    return {
        "minicurso_id": minicurso_id,
        "total_aulas": total_aulas,
        "aulas_concluidas": aulas_concluidas,
        "progresso": round(progresso, 2)
    }