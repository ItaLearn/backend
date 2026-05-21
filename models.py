from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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

    aulas = relationship("Aula", back_populates="minicurso")

class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    id_minicurso = Column(Integer, ForeignKey("minicursos.id"))
    titulo = Column(String, index=True)
    conteudo = Column(String)
    ordem =Column(Integer)

    minicurso = relationship("Minicurso", back_populates="aulas")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Integer)
    comentario = Column(String)

    minicurso_id = Column(Integer, ForeignKey("minicursos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))