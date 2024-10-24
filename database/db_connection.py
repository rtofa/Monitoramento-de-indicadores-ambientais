import mysql.connector

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


