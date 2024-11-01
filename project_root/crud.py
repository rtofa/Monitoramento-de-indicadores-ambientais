from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas
from auth import hash_senha, verificar_senha
from fastapi import HTTPException
import requests

def obter_qualidade_ar(pais: str, estado: str, cidade: str):
    # Define a URL do seu back-end que já faz a consulta na API da IQAir
    url = f'http://localhost:8000/consulta_qualidade_ar/{pais}/{estado}/{cidade}'
    
    
    response = requests.get(url)

   
    if response.status_code == 200:
        return response.json()  
    else:
        return None 

def criar_pesquisa(db: Session, termo: str):
    nova_pesquisa = models.Pesquisa(termo=termo, data_criacao=datetime.utcnow())
    db.add(nova_pesquisa)
    db.commit()
    db.refresh(nova_pesquisa)
    return nova_pesquisa

def listar_pesquisas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Pesquisa).offset(skip).limit(limit).all()

def buscar_pesquisa_por_id(db: Session, pesquisa_id: int):
    pesquisa = db.query(models.Pesquisa).filter(models.Pesquisa.id == pesquisa_id).first()
    if pesquisa is None:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada")
    return pesquisa

def excluir_pesquisa(db: Session, pesquisa_id: int):
    pesquisa = buscar_pesquisa_por_id(db, pesquisa_id)
    if pesquisa:
        db.delete(pesquisa)
        db.commit()
    return pesquisa

# Funções para a tabela Usuario

def criar_usuario(db: Session, username: str, email: str, senha: str):
    senha_hash = hash_senha(senha)  # Cria o hash da senha
    novo_usuario = models.Usuario(username=username, email=email, senha=senha_hash, data_criacao=datetime.utcnow())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def listar_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def buscar_usuario_por_id(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

def buscar_usuario_por_username(db: Session, username: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == username).first()
    return usuario

def autenticar_usuario(db: Session, username: str, senha: str):
    usuario = buscar_usuario_por_username(db, username)
    if usuario and verificar_senha(senha, usuario.senha):
        return usuario
    raise HTTPException(status_code=400, detail="Credenciais incorretas")

def atualizar_usuario(db: Session, usuario_id: int, username: str = None, email: str = None, senha: str = None):
    usuario = buscar_usuario_por_id(db, usuario_id)
    if username:
        usuario.username = username
    if email:
        usuario.email = email
    if senha:
        usuario.senha = hash_senha(senha)
    db.commit()
    db.refresh(usuario)
    return usuario

def excluir_usuario(db: Session, usuario_id: int):
    usuario = buscar_usuario_por_id(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario
