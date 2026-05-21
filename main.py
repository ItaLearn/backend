from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, get_db
import models

from CreateAula import router as create_aula
from ReadAula import router as read_aula
from UpdateAula import router as update_aula
from DeleteAula import router as delete_aula

from CreateUsuario import router as create_usuario

from createMinicurso import router as create_minicurso
from buscarMinicurso import router as buscar_minicurso
from avaliarMinicurso import router as avaliar_minicurso
from listarAvaliacao import router as listar_avaliacao
from deletarAvaliacao import router as deletar_avaliacao

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma de Estudos API")

app.include_router(create_aula)
app.include_router(read_aula)
app.include_router(update_aula)
app.include_router(delete_aula)

app.include_router(create_usuario)

app.include_router(create_minicurso)
app.include_router(buscar_minicurso)
app.include_router(avaliar_minicurso)
app.include_router(listar_avaliacao)
app.include_router(deletar_avaliacao)