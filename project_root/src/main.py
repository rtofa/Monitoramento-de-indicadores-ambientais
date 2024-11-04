import sys
import os
from fastapi import FastAPI, HTTPException
import uvicorn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database import init_db
from services.scraping import obter_aqi_cidade

app = FastAPI()

init_db()


@app.get("/consulta_qualidade_ar/{pais}/{estado}/{cidade}")
def consulta_qualidade_ar(pais: str, estado: str, cidade: str):
    try:
        
        resultado = obter_aqi_cidade(cidade, estado, pais)
        return resultado
    except HTTPException as e:
        
        raise e
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)