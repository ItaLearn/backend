from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, get_db
import models

class CriarUsuario(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    nome_usuario: str = Field(min_length=3, max_length=15)
    email: str
    senha: str
    profissao: str

class FazerLogin(BaseModel):
    email: str
    senha: str

class CriarMinicurso(BaseModel):
    titulo: str
    descricao: str
    autor_email: str

class CriarAula(BaseModel):
    id_minicurso: int
    titulo: str
    conteudo: str
    ordem: int