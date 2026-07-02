from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.post("/minicursos/{minicurso_id}/inscrever")
def inscrever_curso(minicurso_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()

    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")

    inscricao_existente = db.query(models.InscricaoCurso).filter(
        models.InscricaoCurso.usuario_id == usuario_logado.id,
        models.InscricaoCurso.minicurso_id == minicurso_id
    ).first()

    if inscricao_existente:
        raise HTTPException(status_code=400, detail="Usuário já inscrito nesse minicurso")

    nova_inscricao = models.InscricaoCurso(
        usuario_id=usuario_logado.id,
        minicurso_id=minicurso_id
    )

    db.add(nova_inscricao)
    db.commit()

    return {"mensagem": "Inscrição realizada com sucesso"}