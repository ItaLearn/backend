from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from auth import criar_token, verificar_senha
import models

router = APIRouter()

@router.post("/login")
def fazer_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos!")
    
    if not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    
    token = criar_token({"sub": str(usuario.id)})
    
    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        },
        "access_token": token,
        "token_type": "bearer"
    }