import sqlite3
import os
import atexit

# Nome do arquivo do banco de dados
DB_FILE = "scv.db"

# Conexão global
CONN = None

def get_db_connection():
    """
    Cria e retorna a conexão com o banco de dados.
    Inicializa o BD se necessário.
    """
    global CONN
    if CONN is None:
        # Se o BD não existe, o sqlite3.connect() o cria automaticamente
        CONN = sqlite3.connect(DB_FILE)
        print(f"Banco de dados '{DB_FILE}' conectado e/ou criado.")
        # Opcional: registrar a função de limpeza ao fechar a aplicação
        atexit.register(cleanup_database)
        create_tables(CONN)
    return CONN

def create_tables(conn):
    """
    Cria as tabelas iniciais.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY,
            number INTEGER,
            location TEXT,
            plate TEXT,
            model TEXT,
            is_attended INTEGER CHECK (is_attended IN (0, 1)),
            attended_by TEXT,
            attended_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            is_priority INTEGER CHECK (is_priority IN (0, 1))
            );
        
        CREATE INDEX IF NOT EXISTS idx_calls_created_at ON calls(created_at);
        CREATE INDEX IF NOT EXISTS idx_calls_is_attended ON calls(is_attended);
        CREATE INDEX IF NOT EXISTS idx_calls_attended_by ON calls(attended_by);
        CREATE INDEX IF NOT EXISTS idx_calls_is_priority ON calls(is_priority);
    """)
    conn.commit()
    print("Tabelas verificadas/criadas.")

def cleanup_database():
    """
    A função crucial: Fecha a conexão e DELETA o arquivo do BD.
    Esta função é chamada automaticamente ao final da execução (pelo atexit).
    """
    global CONN
    if CONN is not None:
        CONN.close()
        CONN = None
        print("\nConexão com o BD fechada.")
    
    # Verifica se o arquivo existe antes de tentar apagar
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print(f"*** Sucesso: Arquivo do banco de dados '{DB_FILE}' apagado. ***")
        except OSError as e:
            print(f"Erro ao apagar o arquivo do BD: {e}")