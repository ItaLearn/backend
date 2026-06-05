from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CriarAvaliacao
import models

router = APIRouter()

@router.post("/minicursos/{minicurso_id}/avaliacoes")
def criar_avaliacao(minicurso_id: int, avaliacao: CriarAvaliacao, db: Session = Depends(get_db)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()

    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == avaliacao.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário inexistente")

    nova_avaliacao = models.Avaliacao(
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        minicurso_id=minicurso_id,
        usuario_id=avaliacao.usuario_id
    )

    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)

    return {
        "mensagem": "Avaliação criada com sucesso!",
        "id_avaliacao": nova_avaliacao.id
    }