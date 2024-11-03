
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import requests
import uvicorn
from project_root.database.database import get_db, init_db
from project_root import crud, schemas

app = FastAPI()

init_db()

# Endpoint para cadastrar um novo usuário
@app.post("/usuarios/", response_model=schemas.Usuario)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_por_username(db, usuario.username)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Username já cadastrado.")
    return crud.create_usuario(db=db, usuario=usuario)

# Endpoint para obter a lista de usuários
@app.get("/usuarios/", response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.get_usuarios(db)

# Endpoint para obter a qualidade do ar com base na localização
@app.get("/qualidade_ar/{pais}/{estado}/{cidade}", response_model=schemas.QualidadeAr)  # Altere para o schema correto
def obter_qualidade_ar(pais: str, estado: str, cidade: str, db: Session = Depends(get_db)):
    qualidade = crud.obter_qualidade_ar(pais, estado, cidade)
    
    if not qualidade:
        raise HTTPException(status_code=404, detail="Dados de qualidade do ar não encontrados.")
    
    return qualidade

# Endpoint para consultar a qualidade do ar diretamente na API da IQAir
@app.get("/consulta_qualidade_ar/{pais}/{estado}/{cidade}")
def consulta_qualidade_ar(pais: str, estado: str, cidade: str):
    iqair_api_url = f"https://api.iqair.com/v1/data?country={pais}&state={estado}&city={cidade}&key=YOUR_API_KEY"
    
    response = requests.get(iqair_api_url)
    
    if response.status_code == 200:
        return response.json()  # Retorna os dados da IQAir
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao consultar a API da IQAir.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)