"""
from typing import Optional
import requests
from requests.utils import quote
from fastapi import HTTPException

API_KEY = '02adefbf-c576-4cc7-bd0b-c310d359d731'
BASE_URL = 'https://api.airvisual.com/v2'

def obter_paises():
    
    url = f"{BASE_URL}/countries?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            return [pais['country'] for pais in dados['data']]
    raise HTTPException(status_code=500, detail="Erro ao buscar países.")

def obter_estados(pais):
    
    url = f"{BASE_URL}/states?country={quote(pais)}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            return [estado['state'] for estado in dados['data']]
    raise HTTPException(status_code=500, detail="Erro ao buscar estados.")

def obter_cidades(estado, pais):
   
    url = f"{BASE_URL}/cities?state={quote(estado)}&country={quote(pais)}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            return [cidade['city'] for cidade in dados['data']]
    raise HTTPException(status_code=500, detail="Erro ao buscar cidades.")

def obter_aqi_cidade(cidade: Optional[str] = None, estado: Optional[str] = None, pais: Optional[str] = None):
    
     # Construa a URL dinamicamente com base nos parâmetros fornecidos
    url = f"{BASE_URL}/city?"
    if cidade:
        url += f"city={quote(cidade)}&"
    if estado:
        url += f"state={quote(estado)}&"
    if pais:
        url += f"country={quote(pais)}&"
    url += f"key={API_KEY}"

   
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            poluicao = dados['data']['current']['pollution']
            aqi = poluicao['aqius']

            
            avaliacao = avaliar_qualidade_ar(aqi)

            return {
                'cidade': cidade or "Não especificado",
                'estado': estado or "Não especificado",
                'pais': pais or "Não especificado",
                'aqi': aqi,
                **avaliacao
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao obter informações: {dados.get('data', {}).get('message', 'Erro desconhecido')}"
            )
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na requisição para {cidade}, {estado}, {pais}: {response.status_code}"
        )

def avaliar_qualidade_ar(aqi: int) -> dict:
    
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
"""