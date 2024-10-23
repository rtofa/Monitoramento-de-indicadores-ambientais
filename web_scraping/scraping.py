import requests
import csv
import mysql.connector

# Substitua 'YOUR_API_KEY' pela sua chave de API
API_KEY = '02adefbf-c576-4cc7-bd0b-c310d359d731'
BASE_URL = 'https://api.airvisual.com/v2'

def obter_paises():
    """Obter a lista de países disponíveis na API."""
    url = f"{BASE_URL}/countries?key={API_KEY}"
    response = requests.get(url)

    # Verifique o status da resposta
    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        print(f"Resposta do servidor: {response.text}")
        return []

    try:
        dados = response.json()
    except ValueError:
        print("A resposta não é um JSON válido.")
        print(f"Resposta recebida: {response.text}")
        return []

    if dados['status'] == 'success':
        return [pais['country'] for pais in dados['data']]
    else:
        print(f"Erro ao obter países: {dados['data']['message']}")
        return []

def obter_aqi_pais(pais, cidade, estado):

    """Obter a qualidade do ar para uma cidade representativa em um país."""
    
    url = f"{BASE_URL}/city?city={cidade}&state={estado}&country={pais}&key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    if dados['status'] == 'success':
        aqi = dados['data']['current']['pollution']['aqius']
        return aqi
    else:
        print(f"Erro ao obter AQI para {pais}: {dados['data']['message']}")
        return None

def salvar_dados_csv(dados, nome_arquivo='poluicao_paises.csv'):
    """Salvar os dados em formato CSV."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['País', 'AQI'])
        for linha in dados:
            writer.writerow(linha)

def salvar_dados_mysql(dados):
    """Salvar os dados no banco de dados MySQL."""
    conexao = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="root",
        database="ar_saude"
    )
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS poluicao_paises (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pais VARCHAR(255),
            aqi INT,
            data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for pais, aqi in dados:
        cursor.execute(
            "INSERT INTO poluicao_paises (pais, aqi) VALUES (%s, %s)",
            (pais, aqi)
        )
    conexao.commit()
    cursor.close()
    conexao.close()
    print("Dados salvos no banco de dados com sucesso.")

def main():

    cidade = input("Digite o nome de uma cidade para coletar os dados: ")
    estado = input("Digite o nome do estado associado à cidade: ")

    # Obter a lista de países
    paises = obter_paises()
    dados_aqi = []

    # Coletar o AQI para cada país, considerando uma cidade e estado fornecidos manualmente para fazer a requisição da API  para obter os indicadores ambientais gerais
    for pais in paises:
        aqi = obter_aqi_pais(pais,cidade, estado)
        if aqi is not None:
            dados_aqi.append((pais, aqi))

    # Salvar os dados em um arquivo CSV
    salvar_dados_csv(dados_aqi)

    # Salvar os dados no banco de dados MySQL
    salvar_dados_mysql(dados_aqi)

if __name__ == "__main__":
    main()
