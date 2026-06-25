from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean, UniqueConstraint
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
    progressos = relationship("ProgressoAula", back_populates="usuario")
    comentarios = relationship("ComentarioAula", back_populates="usuario")
    like_curso = relationship("LikeCurso", back_populates="usuario")
    inscricoes = relationship("InscricaoCurso", back_populates="usuario")

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
    progressos = relationship("ProgressoAula", back_populates="minicurso")
    like = relationship("LikeCurso", back_populates="minicurso", cascade="all, delete")
    inscricoes = relationship("InscricaoCurso", back_populates="minicurso")

class InscricaoCurso(Base):
    __tablename__ = "inscricoes_cursos"

    __table_args__ = (UniqueConstraint("usuario_id", "minicurso_id", name="uq_usuario_minicurso"),)

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    minicurso_id = Column(Integer, ForeignKey("minicursos.id"))
    usuario = relationship("Usuario", back_populates="inscricoes")
    minicurso = relationship("Minicurso", back_populates="inscricoes")

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
    progressos = relationship("ProgressoAula", back_populates="aula")
    comentarios = relationship("ComentarioAula", back_populates="aula")

class ProgressoAula(Base):
    __tablename__ = "progresso_aulas"

    __table_args__ = (UniqueConstraint("usuario_id", "aula_id", name="uq_usuario_aula"),)

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    aula_id = Column(Integer, ForeignKey("aulas.id"))
    minicurso_id = Column(Integer, ForeignKey("minicursos.id"))
    concluida = Column(Boolean, default=True)
    usuario = relationship("Usuario", back_populates="progressos")
    aula = relationship("Aula", back_populates="progressos")
    minicurso = relationship("Minicurso", back_populates="progressos")

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

class ComentarioAula(Base):
    __tablename__ = "comentarios_aula"

    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    aula_id = Column(Integer, ForeignKey("aulas.id"), nullable=False)
    comentario_pai_id = Column(Integer, ForeignKey("comentarios_aula.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="comentarios")
    aula = relationship("Aula", back_populates="comentarios")
    respostas = relationship("ComentarioAula", backref="comentario_pai", remote_side=[id])

class LikeCurso(Base):
    __tablename__ = "like_curso"

    __table_args__ = (UniqueConstraint("usuario_id", "minicurso_id", name="uq_usuario_like_curso"),)

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    minicurso_id = Column(Integer, ForeignKey("minicursos.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="like_curso")
    minicurso = relationship("Minicurso", back_populates="like")