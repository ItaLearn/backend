from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_logado
import models

router = APIRouter()

@router.get("/meus-cursos")
def listar_meus_cursos(db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_usuario_logado)):
    inscricoes = db.query(models.InscricaoCurso).filter(models.InscricaoCurso.usuario_id == usuario_logado.id).all()

    cursos = [inscricao.minicurso for inscricao in inscricoes]

    return cursos