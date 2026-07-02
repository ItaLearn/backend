from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.get("/meu-perfil")
def meu_perfil(usuario_logado: models.Usuario = Depends(get_usuario_logado), db: Session = Depends(get_db)):
    progressos = db.query(models.ProgressoAula).filter(models.ProgressoAula.usuario_id == usuario_logado.id).all()
    avaliacoes = db.query(models.Avaliacao).filter(models.Avaliacao.usuario_id == usuario_logado.id).all()
    comentarios = db.query(models.ComentarioAula).filter(models.ComentarioAula.usuario_id == usuario_logado.id).all()

    return {
        "usuario": {
            "id": usuario_logado.id,
            "nome": usuario_logado.nome,
            "nome_usuario": usuario_logado.nome_usuario,
            "email": usuario_logado.email,
            "profissao": usuario_logado.profissao
        },
        "progresso_minicursos": progressos,
        "avaliacoes": avaliacoes,
        "comentarios": comentarios
    }