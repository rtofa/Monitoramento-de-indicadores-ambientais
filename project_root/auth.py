import bcrypt


def hash_senha(senha: str) -> str:
    
    salt = bcrypt.gensalt()
    
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hash.decode('utf-8')  # Retorna como string


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))