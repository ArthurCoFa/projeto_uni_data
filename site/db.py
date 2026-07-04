import mysql.connector

PER_PAGE = 5

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Arthur22012007", # Sua Senha do Banco
        database="uni_data"
    )

def contar_registros(tabela, busca=None, campo_busca='nome'):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if busca:
        if str(busca).isdigit():
            query = f"SELECT COUNT(*) as total FROM {tabela} WHERE {campo_busca} LIKE %s"
            cursor.execute(query, (busca,))
        else:
            query = f"SELECT COUNT(*) as total FROM {tabela} WHERE {campo_busca} LIKE %s"
            cursor.execute(query, ('%' + busca + '%',))
    else:
        query = f"SELECT COUNT(*) as total FROM {tabela}"
        cursor.execute(query)
        
    resultado = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return resultado['total']