from pydantic import BaseModel
from datetime import datetime

class UsuarioBase(BaseModel):
    username: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str  # Senha deve ser incluída apenas na criação

class Usuario(UsuarioBase):
    id: int
    data_criacao: datetime

    class Config:
        orm_mode = True
