from fastapi import APIRouter, FastAPI, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from cloudinary_service import upload_arquivo
import models

router = APIRouter()

@router.post("/minicurso/{id_minicurso}/aula")
def criar_aula(id_minicurso: int, titulo: str = Form(...), conteudo: UploadFile = File(...), db: Session = Depends(get_db)):
    minicurso = db.query(models.Minicurso).filter(models.Minicurso.id == id_minicurso).first()

    if not minicurso:
        raise HTTPException(status_code=404, detail="Minicurso não encontrado")
    
    ultima_aula = db.query(models.Aula).filter(models.Aula.id_minicurso == id_minicurso).order_by(models.Aula.ordem.desc()).first()

    nova_ordem = 1 if not ultima_aula else ultima_aula.ordem + 1

    try:
        url = upload_arquivo(conteudo.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")


    nova_aula = models.Aula(
        titulo = titulo,
        conteudo = url,
        ordem = nova_ordem,
        id_minicurso = id_minicurso
    )

    db.add(nova_aula)
    db.commit()
    db.refresh(nova_aula)

    return nova_aula