from sqlalchemy import Column, DateTime, Integer, String
from project_root.database import Base 
from datetime import datetime


class Pesquisa(Base):
        __tablename__ = 'pesquisas'  # Nome da tabela existente

        id = Column(Integer, primary_key=True, index=True)
        termo = Column(String(255), index=True)
        data_criacao = Column(DateTime)

        def __repr__(self):
            return f"<Pesquisa(termo='{self.termo}', data_criacao='{self.data_criacao}')>"


class Usuario(Base):
        __tablename__ = 'usuarios'  

        id = Column(Integer, primary_key=True, index=True)
        username = Column(String(100), unique=True, index=True, nullable=False)  
        email = Column(String(255), unique=True, index=True, nullable=False) 
        senha = Column(String(100), nullable=False)  
        data_criacao = Column(DateTime, default=datetime.utcnow)  
        
        def __repr__(self):
            return f"<Usuario(username='{self.username}', email='{self.email}', data_criacao='{self.data_criacao}')>"
