import requests
import csv
import time
from src.db_connection import salvar_dados_mysql
from requests.utils import quote

API_KEY = '02adefbf-c576-4cc7-bd0b-c310d359d731'
BASE_URL = 'https://api.airvisual.com/v2'


def obter_paises():
    url = f"{BASE_URL}/countries?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            return [pais['country'] for pais in dados['data']]
    print("Erro ao buscar países.")
    return []


def obter_estados(pais):
    url = f"{BASE_URL}/states?country={quote(pais)}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            return [estado['state'] for estado in dados['data']]
    print("Erro ao buscar estados.")
    return []


def obter_cidades(estado, pais):
    url = f"{BASE_URL}/cities?state={quote(estado)}&country={quote(pais)}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados['status'] == 'success':
            return [cidade['city'] for cidade in dados['data']]
    print("Erro ao buscar cidades.")
    return []


def escolher_pais():
    paises = obter_paises()
    if not paises:
        print("Nenhum país disponível.")
        return None
    print("Países disponíveis:")
    for i, pais in enumerate(paises):
        print(f"{i + 1}. {pais}")
    escolha = int(input("Escolha um país (digite o número): ")) - 1
    if 0 <= escolha < len(paises):
        return paises[escolha]
    else:
        print("Escolha inválida.")
        return None


def escolher_estado(pais):
    estados = obter_estados(pais)
    if not estados:
        print("Nenhum estado disponível.")
        return None
    print("Estados disponíveis:")
    for i, estado in enumerate(estados):
        print(f"{i + 1}. {estado}")
    escolha = int(input("Escolha um estado (digite o número): ")) - 1
    if 0 <= escolha < len(estados):
        return estados[escolha]
    else:
        print("Escolha inválida.")
        return None


def escolher_cidade(estado, pais):
    cidades = obter_cidades(estado, pais)
    if not cidades:
        print("Nenhuma cidade disponível.")
        return None
    print("Cidades disponíveis:")
    for i, cidade in enumerate(cidades):
        print(f"{i + 1}. {cidade}")
    escolha = int(input("Escolha uma cidade (digite o número): ")) - 1
    if 0 <= escolha < len(cidades):
        return cidades[escolha]
    else:
        print("Escolha inválida.")
        return None


def obter_aqi_cidade(cidade, estado, pais):

    """Obter a qualidade do ar para uma cidade específica."""

    
    pais_codificado = quote(pais)
    estado_codificado = quote(estado)
    cidade_codificada = quote(cidade)
    
    url = f"{BASE_URL}/city?city={cidade_codificada}&state={estado_codificado}&country={pais_codificado}&key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro na requisição para {cidade}, {estado}, {pais}: {response.status_code}")
        return None

    dados = response.json()
    
    if dados['status'] == 'success':
        poluicao = dados['data']['current']['pollution']
        aqi = poluicao['aqius']  # AQI para poluição por PM2.5
        # Adicione as recomendações com base no AQI
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

        return {
            'cidade': cidade,
            'estado': estado,
            'pais': pais,
            'aqi': aqi,
            'seguranca': seguranca,
            'recomendacao': recomendacao
        }
    else:
        print(f"Erro ao obter informações: {dados.get('data', {}).get('message', 'Erro desconhecido')}")
        return None



def salvar_dados_csv(dados, nome_arquivo='dados_poluicao.csv'):

    """Salvar os dados em formato CSV."""

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cidade', 'Estado', 'País', 'AQI'])
        for linha in dados:
            writer.writerow(linha)


def monitorar_qualidade_do_ar(cidade, estado, pais):

    """Monitorar continuamente a qualidade do ar em uma cidade específica."""

    while True:
        informacoes = obter_aqi_cidade(cidade, estado, pais)
        
        if informacoes is not None:
            aqi = informacoes['aqi']
            seguranca = informacoes['seguranca']
            recomendacao = informacoes['recomendacao']
            
            print(f"Qualidade do ar em {informacoes['cidade']}, {informacoes['estado']}, {informacoes['pais']}:")
            print(f"AQI: {aqi}")
            print(f"Segurança: {seguranca}")
            print(f"Recomendação: {recomendacao}")
            
            dados_aqi = [(informacoes['cidade'], informacoes['estado'], informacoes['pais'], aqi)]
            salvar_dados_csv(dados_aqi)
            salvar_dados_mysql(dados_aqi)

        # Intervalo entre verificações (por exemplo, 1 hora)
        time.sleep(3600)


    
