from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/usuarios/{usuario_id}/favoritos")
def listar_favoritos(usuario_id: int, db: Session = Depends(get_db)):

    favoritos = db.query(models.Favorito).filter(models.Favorito.usuario_id == usuario_id).all()

    return favoritos