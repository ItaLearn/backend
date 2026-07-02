from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.get("/usuarios/favoritos")
def listar_favoritos(db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):

    favoritos = db.query(models.Favorito).filter(models.Favorito.usuario_id == usuario_logado.id).all()

    return favoritos