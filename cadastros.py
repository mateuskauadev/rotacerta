from banco import conectar
import pandas as pd


def cadastrar_cliente(nome, cidade, estado):
    with conectar() as conn:
        conn.execute("INSERT INTO clientes (nome, cidade, estado) VALUES (?, ?, ?)", (nome, cidade, estado))


def listar_clientes():
    with conectar() as conn:
        return pd.read_sql("SELECT * FROM clientes", conn)


def cadastrar_caminhao(placa, modelo, capacidade):
    with conectar() as conn:
        conn.execute("INSERT INTO caminhoes (placa, modelo, capacidade_kg) VALUES (?, ?, ?)", (placa, modelo, capacidade))


def listar_caminhoes():
    with conectar() as conn:
        return pd.read_sql("SELECT * FROM caminhoes", conn)

def cadastrar_entrega(cliente_id, caminhao_id, peso_kg, data_saida, prazo):
    with conectar() as conn:
        conn.execute("INSERT INTO entregas(cliente_id, caminhao_id, peso_kg, data_saida, prazo) VALUES (?, ?, ?, ?, ?) ", (cliente_id, caminhao_id, peso_kg, data_saida, prazo))

def listar_entregas():
    with conectar() as conn:
        return pd.read_sql("SELECT * FROM entregas", conn)

def registrar_chegada(entrega_id, data_entrega):
    with conectar() as conn:
        conn.execute("UPDATE entregas SET data_entrega = ? WHERE id = ?", (data_entrega, entrega_id))

