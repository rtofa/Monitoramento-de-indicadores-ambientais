import requests

def obter_qualidade_ar(pais: str, estado: str, cidade: str):
   
    url = f'http://localhost:8000/consulta_qualidade_ar/{pais}/{estado}/{cidade}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return None 
