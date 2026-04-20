from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50))
    nome_usuario = Column(String(15), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    profissao = Column(String)

class Minicurso(Base):
    __tablename__ = "minicursos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String)
    autor_email = Column(String)