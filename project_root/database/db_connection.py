import mysql.connector
from exceptions import DatabaseError

def salvar_dados_mysql(dados):
    """Salvar os dados no banco de dados MySQL."""
    try:
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
        for pais, cidade, estado, aqi in dados:
            cursor.execute(
                "INSERT INTO poluicao_paises (pais, aqi) VALUES (%s, %s)",
                (pais, cidade, estado, aqi)
            )
        conexao.commit()

    except mysql.connector.Error as e:
        raise DatabaseError(f"Erro ao salvar no banco de dados: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()
        print("Conexão com o banco de dados encerrada.")


