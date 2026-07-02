from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.delete("/avaliacoes/{avaliacao_id}")
def excluir_avaliacao(avaliacao_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    avaliacao = db.query(models.Avaliacao).filter(
        models.Avaliacao.id == avaliacao_id
    ).first()

    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    if avaliacao.usuario_id != usuario_logado.id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para excluir esta avaliação"
        )

    db.delete(avaliacao)
    db.commit()

    return {"mensagem": "Avaliação excluída com sucesso!"}