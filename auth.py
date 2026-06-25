from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
import models
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def criar_token(dados: dict):
    dados_copia = dados.copy()

    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_copia.update({"exp": expiracao})

    token = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_usuario_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(usuario_id)).first()

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return usuario


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash_senha(senha: str):
    return pwd_context.hash(str(senha))

def verificar_senha(senha_digitada: str, senha_hash: str):
    return pwd_context.verify(senha_digitada, senha_hash)