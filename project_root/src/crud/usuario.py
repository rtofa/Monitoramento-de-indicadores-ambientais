from sqlalchemy.orm import Session
from datetime import datetime
from project_root import models
from project_root.src.auth import hash_senha, verificar_senha
from fastapi import HTTPException

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
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()

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
