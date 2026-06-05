from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CriarFavorito
import models

router = APIRouter()

@router.post("/minicursos/{minicurso_id}/favoritar")
def favoritar_minicurso(minicurso_id: int, favorito: CriarFavorito, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == favorito.usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == minicurso_id).first()

    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")

    favorito_existente = db.query(models.Favorito).filter(
        models.Favorito.usuario_id == favorito.usuario_id,
        models.Favorito.minicurso_id == minicurso_id).first()

    if favorito_existente:
        raise HTTPException(status_code=400, detail="Minicurso já está nos favoritos")

    novo_favorito = models.Favorito(usuario_id=favorito.usuario_id, minicurso_id=minicurso_id)

    db.add(novo_favorito)
    db.commit()

    return {"mensagem": "Minicurso favoritado com sucesso!"}