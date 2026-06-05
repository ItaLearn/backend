from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import SolicitarRedefinicaoSenha
from email_service import enviar_email_redefinicao
from database import get_db
import models
import secrets
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/esqueci-senha")
async def esqueci_senha(dados: SolicitarRedefinicaoSenha, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="E-mail não encontrado")

    token = secrets.token_urlsafe(32)

    usuario.token_redefinicao = token
    usuario.token_expira = datetime.utcnow() + timedelta(minutes=30)

    db.commit()

    await enviar_email_redefinicao(usuario.email, token)

    return {
        "mensagem": "Token de redefinição gerado com sucesso",
        "token": token
    }