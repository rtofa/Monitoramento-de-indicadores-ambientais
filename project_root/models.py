from sqlalchemy import Column, DateTime, Integer, String
from .database import Base 
from datetime import datetime


class Pesquisa(Base):
        __tablename__ = 'pesquisas'  # Nome da tabela existente

        id = Column(Integer, primary_key=True, index=True)
        termo = Column(String, index=True)
        data_criacao = Column(DateTime)

        def __repr__(self):
            return f"<Pesquisa(termo='{self.termo}', data_criacao='{self.data_criacao}')>"


class Usuario(Base):
        __tablename__ = 'usuarios'  

        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True, index=True)  
        email = Column(String, unique=True, index=True) 
        senha = Column(String)  
        data_criacao = Column(DateTime, default=datetime.utcnow)  
        
        def __repr__(self):
            return f"<Usuario(username='{self.username}', email='{self.email}', data_criacao='{self.data_criacao}')>"
