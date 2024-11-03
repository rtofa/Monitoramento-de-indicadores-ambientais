from pydantic import BaseModel
from datetime import datetime

class QualidadeAr(BaseModel):
    pais: str
    estado: str
    cidade: str
    qualidade: int  # Exemplo de como você pode querer descrever a qualidade do ar
    data_hora: datetime  # Data e hora da consulta

    class Config:
        orm_mode = True
