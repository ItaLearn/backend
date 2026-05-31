from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import FazerLogin
import models

router = APIRouter()

@router.post("/login")
def fazer_login(credenciais: FazerLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == credenciais.email).first()
    
    if not usuario or usuario.senha != credenciais.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos!")
    
    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }