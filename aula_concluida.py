from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.post("/aulas/{aula_id}/concluir")
def concluir_aula(aula_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    aula = db.query(models.Aula).filter(models.Aula.id == aula_id).first()

    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")

    progresso_existente = db.query(models.ProgressoAula).filter(
        models.ProgressoAula.usuario_id == usuario_logado.id,
        models.ProgressoAula.aula_id == aula_id
    ).first()

    if progresso_existente:
        return {"mensagem": "Aula já estava concluída"}

    progresso = models.ProgressoAula(
        usuario_id=usuario_logado.id,
        aula_id=aula.id,
        minicurso_id=aula.id_minicurso,
        concluida=True
    )

    db.add(progresso)
    db.commit()

    return {"mensagem": "Aula concluída com sucesso"}