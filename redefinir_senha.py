from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import RedefinirSenha
from database import get_db
import models
from datetime import datetime

router = APIRouter()

@router.post("/redefinir-senha")
def redefinir_senha(dados: RedefinirSenha, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.token_redefinicao == dados.token).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Token inválido")

    if usuario.token_expira < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado")

    usuario.senha = dados.nova_senha

    usuario.token_redefinicao = None
    usuario.token_expira = None

    db.commit()

    return {"mensagem": "Senha redefinida com sucesso"}