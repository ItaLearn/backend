from fastapi import FastAPI
from database import engine
import models

from createMinicurso import router as create_minicurso
from readMinicurso import router as read_minicurso
from updateMinicurso import router as update_minicurso
from deleteMinicurso import router as delete_minicurso

from ReadAula import router as read_aula

from createUser import router as create_usuario
from readUser import router as read_usuario
from updateUser import router as update_usuario
from deleteUser import router as delete_usuario
from loginUser import router as login_usuario

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma de Estudos API")

app.include_router(create_usuario)
app.include_router(read_usuario)
app.include_router(update_usuario)
app.include_router(delete_usuario)
app.include_router(login_usuario)

app.include_router(create_minicurso)
app.include_router(read_minicurso)
app.include_router(update_minicurso)
app.include_router(delete_minicurso)

app.include_router(read_aula)
