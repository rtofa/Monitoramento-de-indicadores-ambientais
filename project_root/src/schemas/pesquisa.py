from pydantic import BaseModel
from datetime import datetime

class PesquisaBase(BaseModel):
    termo: str
    data_criacao: datetime

class PesquisaCreate(PesquisaBase):
    pass

class Pesquisa(PesquisaBase):
    id: int

    class Config:
        orm_mode = True
