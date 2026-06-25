from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CriarComentario
from auth import get_usuario_logado
import models

router = APIRouter()

@router.post("/aulas/{aula_id}/comentarios")
def criar_comentario(aula_id: int, comentario: CriarComentario, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    aula = db.query(models.Aula).filter(models.Aula.id == aula_id).first()

    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")

    if comentario.comentario_pai_id:
        comentario_pai = db.query(models.ComentarioAula).filter(
            models.ComentarioAula.id == comentario.comentario_pai_id,
            models.ComentarioAula.aula_id == aula_id
        ).first()

        if not comentario_pai:
            raise HTTPException(status_code=404, detail="Comentário não encontrado")

    novo_comentario = models.ComentarioAula(
        conteudo = comentario.conteudo,
        aula_id = aula_id,
        usuario_id = usuario_logado.id,
        comentario_pai_id = comentario.comentario_pai_id
    )

    db.add(novo_comentario)
    db.commit()
    db.refresh(novo_comentario)

    return {
        "mensagem": "Comentário criado com sucesso",
        "comentario": novo_comentario
    }