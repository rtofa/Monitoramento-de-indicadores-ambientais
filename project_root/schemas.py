from pydantic import BaseModel
from datetime import datetime


# Schema para Usuario
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

# Schema para Pesquisa
class PesquisaBase(BaseModel):
    termo: str
    data_criacao: datetime

class PesquisaCreate(PesquisaBase):
    pass

class Pesquisa(PesquisaBase):
    id: int

    class Config:
        orm_mode = True

# Schema para Qualidade do Ar
class QualidadeAr(BaseModel):
    pais: str
    estado: str
    cidade: str
    qualidade: int  # Exemplo de como você pode querer descrever a qualidade do ar
    data_hora: datetime  # Data e hora da consulta

    class Config:
        orm_mode = True
