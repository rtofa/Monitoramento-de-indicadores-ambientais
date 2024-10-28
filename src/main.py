
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraping import escolher_pais, escolher_estado, escolher_cidade, monitorar_qualidade_do_ar
from exceptions import APIError, DatabaseError

if __name__ == "__main__":
    try:
        pais = escolher_pais()
        if not pais:
            sys.exit("Processo interrompido: país não selecionado.")
            exit()

        estado = escolher_estado(pais)
        if not estado:
            sys.exit("Processo interrompido: estado não selecionado.")
            exit()

        cidade = escolher_cidade(estado, pais)
        if not cidade:
            sys.exit("Processo interrompido: cidade não selecionada.")
            exit()
    
            print(f"Você escolheu: {cidade}, {estado}, {pais}")
            monitorar_qualidade_do_ar(cidade, estado, pais)

        
    except APIError as e:
        print(f"Erro ao acessar a API: {str(e)}")
    except DatabaseError as e:
        print(f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")