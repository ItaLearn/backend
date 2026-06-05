from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
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
    minicursos = relationship("Minicurso", back_populates="autor")
    token_redefinicao = Column(String, nullable=True)
    token_expira = Column(DateTime, nullable=True)

curso_categoria = Table(
    "curso_categoria",
    Base.metadata,
    Column("curso_id", Integer, ForeignKey("minicursos.id")),
    Column("categoria_id", Integer, ForeignKey("categorias.id"))
)

class Minicurso(Base):
    __tablename__ = "minicursos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String)
    autor_id = Column(Integer, ForeignKey("usuarios.id"))
    autor = relationship("Usuario", back_populates="minicursos")
    aulas = relationship("Aula", back_populates="minicurso")
    categorias = relationship("Categoria", secondary=curso_categoria, back_populates="cursos")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    cursos = relationship("Minicurso", secondary=curso_categoria, back_populates="categorias")

class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    id_minicurso = Column(Integer, ForeignKey("minicursos.id"))
    titulo = Column(String, index=True)
    conteudo = Column(String)
    ordem = Column(Integer)
    minicurso = relationship("Minicurso", back_populates="aulas")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Integer)
    comentario = Column(String)
    minicurso_id = Column(Integer, ForeignKey("minicursos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

class Favorito(Base):
    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    minicurso_id = Column(Integer, ForeignKey("minicursos.id"))