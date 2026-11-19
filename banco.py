import sqlite3

ARQUIVO_BANCO = "rotacerta.db"


def conectar():
    """Abre a conexão com o banco e liga as chaves estrangeiras."""
    conn = sqlite3.connect(ARQUIVO_BANCO)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    """Cria as tabelas do sistema, se ainda não existirem."""
    with conectar() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS clientes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nome    TEXT NOT NULL,
                cidade  TEXT NOT NULL,
                estado  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS caminhoes (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                placa          TEXT NOT NULL UNIQUE,
                modelo         TEXT NOT NULL,
                capacidade_kg  REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS entregas (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id    INTEGER NOT NULL REFERENCES clientes(id),
                caminhao_id   INTEGER NOT NULL REFERENCES caminhoes(id),
                peso_kg       REAL NOT NULL,
                data_saida    TEXT NOT NULL,
                prazo         TEXT NOT NULL,
                data_entrega  TEXT
            );
        """)


if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso!")