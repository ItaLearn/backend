from pydantic import BaseModel, Field
from typing import List

class CriarUsuario(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    nome_usuario: str = Field(min_length=3, max_length=15)
    email: str
    senha: str
    profissao: str

class FazerLogin(BaseModel):
    email: str
    senha: str

class SolicitarRedefinicaoSenha(BaseModel):
    email: str

class RedefinirSenha(BaseModel):
    token: str
    nova_senha: str

class CriarMinicurso(BaseModel):
    titulo: str
    descricao: str
    categorias: List[int]

class CriarAula(BaseModel):
    id_minicurso: int
    titulo: str
    conteudo: str
    ordem: int

class CriarAvaliacao(BaseModel):
    nota: int = Field(ge=1, le=5)
    comentario: str
    usuario_id: int

class CriarFavorito(BaseModel):
    usuario_id: int