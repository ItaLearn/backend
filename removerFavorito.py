from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.delete("/minicursos/{minicurso_id}/favoritar")
def remover_favorito(
    minicurso_id: int,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    favorito = db.query(models.Favorito).filter(
        models.Favorito.usuario_id == usuario_id,
        models.Favorito.minicurso_id == minicurso_id
    ).first()

    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")

    db.delete(favorito)
    db.commit()

    return {"mensagem": "Minicurso removido dos favoritos"}