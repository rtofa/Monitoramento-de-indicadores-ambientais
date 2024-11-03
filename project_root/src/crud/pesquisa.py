from sqlalchemy.orm import Session
from datetime import datetime
from project_root import models
from fastapi import HTTPException

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
