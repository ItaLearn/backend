from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from cloudinary_service import upload_arquivo
import models

router = APIRouter()

@router.put("/{id_aula}")
def atualizar_aula(id_aula: int, titulo: str = Form(None), arquivo: UploadFile = File(None), link: str = Form(None), db: Session = Depends(get_db)):
    aula_db = db.query(models.Aula).filter(models.Aula.id == id_aula).first()
    if not aula_db:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    
    if titulo:
        aula_db.titulo = titulo

    if arquivo:
        try:
            url = upload_arquivo(arquivo.file)
            aula_db.conteudo = url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")
        
    elif link:
        aula_db.conteudo = link
        
    db.commit()
    db.refresh(aula_db)
    return aula_db