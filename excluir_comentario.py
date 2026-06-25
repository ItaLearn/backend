from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.delete("/comentarios/{comentario_id}")
def excluir_comentario(comentario_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    comentario = db.query(models.ComentarioAula).filter(models.ComentarioAula.id == comentario_id).first()

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    dono_comentario = comentario.usuario_id == usuario_logado.id
    autor_minicurso = comentario.aula.minicurso.autor_id == usuario_logado.id

    if not dono_comentario and not autor_minicurso:
        raise HTTPException(
            status_code=403,
            detail="Você só pode excluir seus próprios comentários"
        )

    db.delete(comentario)
    db.commit()

    return {"mensagem": "Comentário excluído com sucesso"}