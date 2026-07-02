from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.delete("/minicursos/{minicurso_id}/desinscrever")
def desinscrever_curso(minicurso_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    inscricao = db.query(models.InscricaoCurso).filter(
        models.InscricaoCurso.usuario_id == usuario_logado.id,
        models.InscricaoCurso.minicurso_id == minicurso_id
    ).first()

    if not inscricao:
        raise HTTPException(status_code=404, detail="Usuário não está inscrito nesse minicurso")

    db.delete(inscricao)
    db.commit()

    return {"mensagem": "Inscrição cancelada com sucesso"}