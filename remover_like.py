from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.delete("/minicursos/{minicurso_id}/like")
def remover_like(minicurso_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    like = db.query(models.LikeCurso).filter(
        models.LikeCurso.usuario_id == usuario_logado.id,
        models.LikeCurso.minicurso_id == minicurso_id
    ).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like não encontrado")

    db.delete(like)
    db.commit()

    return {"mensagem": "Like removido com sucesso"}