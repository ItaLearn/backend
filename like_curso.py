from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.post("/minicursos/{minicurso_id}/like")
def like(minicurso_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    curso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()

    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    like_existente = db.query(models.LikeCurso).filter(
        models.LikeCurso.usuario_id == usuario_logado.id,
        models.LikeCurso.minicurso_id == minicurso_id
    ).first()

    if like_existente:
        raise HTTPException(status_code=400, detail="Usuário já curtiu este curso")

    novo_like = models.LikeCurso(
        usuario_id=usuario_logado.id,
        minicurso_id=minicurso_id
    )

    db.add(novo_like)
    db.commit()

    return {"mensagem": "Curso curtido com sucesso"}