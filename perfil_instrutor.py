from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/instrutores/{usuario_id}/perfil")
def perfil_publico_instrutor(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    minicursos = db.query(models.Minicurso).filter(models.Minicurso.autor_id == usuario_id).all()

    return {
        "nome": usuario.nome,
        "nome_usuario": usuario.nome_usuario,
        "profissao": usuario.profissao,
        "minicursos": minicursos
    }