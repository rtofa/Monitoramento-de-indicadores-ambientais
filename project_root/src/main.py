from shlex import quote
import sys
import os
from typing import List, Optional
import requests
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.database import init_db


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens, mas é possível especificar apenas os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"]   # Permite todos os cabeçalhos
)

init_db()

API_KEY = '02adefbf-c576-4cc7-bd0b-c310d359d731'
BASE_URL = 'https://api.airvisual.com/v2'

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

@app.get("/obter-cidades-estado")
def obter_cidades_estado(estado: str):
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
        
@app.get("/obter-aqi")
def obter_aqi(cidade: str, estado: str):
    """Obter a qualidade do ar (AQI) para uma cidade específica em um estado do Brasil"""
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)