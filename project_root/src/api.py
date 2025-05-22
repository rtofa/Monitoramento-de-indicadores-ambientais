from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from project_root.database.database import get_db
from project_root.src import crud
from project_root.src.schemas import Usuario, UsuarioCreate, Pesquisa, PesquisaCreate, QualidadeAr
import requests


API_KEY = '02adefbf-c576-4cc7-bd0b-c310d359d731'
BASE_URL = 'https://api.airvisual.com/v2'


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Não encontrado"}},
)


def avaliar_qualidade_ar(aqi: int):
    if aqi <= 50:
        seguranca = "Boa"
        recomendacao = "Atividades ao ar livre são seguras."
    elif aqi <= 100:
        seguranca = "Moderada"
        recomendacao = "Atividades ao ar livre são aceitáveis, mas sensíveis podem ter problemas."
    elif aqi <= 150:
        seguranca = "Não seguro"
        recomendacao = "Evite atividades ao ar livre."
    else:
        seguranca = "Perigoso"
        recomendacao = "Atividades ao ar livre devem ser evitadas."

    return {"seguranca": seguranca, "recomendacao": recomendacao}


@router.post("/usuarios/", response_model=Usuario)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Criar um novo usuário"""
    db_usuario = crud.buscar_usuario_por_username(db, username=usuario.username)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    return crud.criar_usuario(db=db, username=usuario.username, email=usuario.email, senha=usuario.senha)

@router.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar todos os usuários"""
    usuarios = crud.listar_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obter um usuário específico pelo ID"""
    return crud.buscar_usuario_por_id(db, usuario_id=usuario_id)

@router.put("/usuarios/{usuario_id}", response_model=Usuario)
def atualizar_usuario(
    usuario_id: int, 
    username: Optional[str] = None, 
    email: Optional[str] = None, 
    senha: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """Atualizar dados de um usuário"""
    return crud.atualizar_usuario(db, usuario_id=usuario_id, username=username, email=email, senha=senha)

@router.delete("/usuarios/{usuario_id}", response_model=Usuario)
def excluir_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Excluir um usuário"""
    return crud.excluir_usuario(db, usuario_id=usuario_id)

# Rotas para pesquisas
@router.post("/pesquisas/", response_model=Pesquisa)
def criar_pesquisa(pesquisa: PesquisaCreate, db: Session = Depends(get_db)):
    """Criar uma nova pesquisa"""
    return crud.criar_pesquisa(db=db, termo=pesquisa.termo)

@router.get("/pesquisas/", response_model=List[Pesquisa])
def listar_pesquisas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar todas as pesquisas"""
    pesquisas = crud.listar_pesquisas(db, skip=skip, limit=limit)
    return pesquisas

@router.get("/pesquisas/{pesquisa_id}", response_model=Pesquisa)
def obter_pesquisa(pesquisa_id: int, db: Session = Depends(get_db)):
    """Obter uma pesquisa específica pelo ID"""
    return crud.buscar_pesquisa_por_id(db, pesquisa_id=pesquisa_id)

@router.delete("/pesquisas/{pesquisa_id}", response_model=Pesquisa)
def excluir_pesquisa(pesquisa_id: int, db: Session = Depends(get_db)):
    """Excluir uma pesquisa"""
    return crud.excluir_pesquisa(db, pesquisa_id=pesquisa_id)

# Rotas para qualidade do ar
@router.get("/qualidade-ar/cidades/{estado}")
def obter_cidades_estado(estado: str):
    """Obter lista de cidades disponíveis para um estado"""
    url = f"{BASE_URL}/cities?state={estado}&country=Brazil&key={API_KEY}"

    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            cidades = [cidade['city'] for cidade in dados['data']]
            return {"cidades": cidades}
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao obter cidades: {dados.get('data', {}).get('message', 'Erro desconhecido')}"
            )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Erro ao fazer a requisição para a API IQAir"
        )

@router.get("/qualidade-ar/aqi")
def obter_aqi(cidade: str, estado: str):
    """Obter a qualidade do ar (AQI) para uma cidade específica"""
    url = f"{BASE_URL}/city?city={cidade}&state={estado}&country=Brazil&key={API_KEY}"

    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            aqi = dados['data']['current']['pollution']['aqius']
            avaliacao = avaliar_qualidade_ar(aqi)
            return {
                "cidade": cidade,
                "estado": estado,
                "aqi": aqi,
                **avaliacao
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao obter AQI: {dados.get('data', {}).get('message', 'Erro desconhecido')}"
            )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Erro ao fazer a requisição para a API IQAir"
        )