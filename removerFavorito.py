from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.delete("/minicursos/{minicurso_id}/favoritar")
def remover_favorito(minicurso_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    favorito = db.query(models.Favorito).filter(
        models.Favorito.usuario_id == usuario_logado.id,
        models.Favorito.minicurso_id == minicurso_id
    ).first()

    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")

    db.delete(favorito)
    db.commit()

    return {"mensagem": "Minicurso removido dos favoritos"}