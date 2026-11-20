import os

from banco import criar_tabelas, ARQUIVO_BANCO
from cadastros import (
    cadastrar_cliente, listar_clientes,
    cadastrar_caminhao, listar_caminhoes,
    cadastrar_entrega, listar_entregas,
    registrar_chegada,
)

CLIENTES = [
    ("Mercado Bom Preço", "Rio de Janeiro", "RJ"),
    ("Supermercado Guanabara", "Rio de Janeiro", "RJ"),
    ("Drogaria Vida Leve", "Niterói", "RJ"),
    ("Atacadão Paulista", "São Paulo", "SP"),
    ("Casa do Construtor Minas", "Belo Horizonte", "MG"),
    ("Hortifruti Serra Verde", "Petrópolis", "RJ"),
]

CAMINHOES = [
    ("RIO1A23", "Volvo FH 540", 25000),
    ("KXP2B45", "Mercedes Atego 2430", 14000),
    ("LTN3C67", "VW Delivery 11.180", 8000),
    ("QRS4D89", "Iveco Daily 35-150", 3500),
]

ENTREGAS = [
    (1, 1, 8000,  "2026-11-03", "2026-11-05"),
    (2, 2, 5000,  "2026-11-04", "2026-11-06"),
    (3, 4, 1200,  "2026-11-05", "2026-11-06"),
    (4, 1, 18000, "2026-11-06", "2026-11-10"),
    (5, 3, 6000,  "2026-11-07", "2026-11-11"),
    (6, 4, 2500,  "2026-11-09", "2026-11-10"),
    (1, 2, 9000,  "2026-11-10", "2026-11-12"),
    (3, 1, 22000, "2026-11-11", "2026-11-15"),
    (2, 3, 4000,  "2026-11-13", "2026-11-14"),
    (5, 4, 3000,  "2026-11-16", "2026-11-17"),
    (4, 2, 12000, "2026-11-17", "2026-11-21"),
    (6, 3, 7000,  "2026-11-18", "2026-11-20"),
    (1, 1, 15000, "2026-11-19", "2026-11-21"),
    (3, 4, 2000,  "2026-11-15", "2026-11-17"),
]

CHEGADAS = [
    (1, "2026-11-05"),
    (2, "2026-11-08"),
    (3, "2026-11-06"),
    (4, "2026-11-09"),
    (5, "2026-11-13"),
    (6, "2026-11-10"),
    (7, "2026-11-12"),
    (8, "2026-11-17"),
    (9, "2026-11-14"),
    (10, "2026-11-18"),
]


def popular_banco():
    """Apaga o banco (se existir), recria as tabelas e cadastra os dados de exemplo."""
    if os.path.exists(ARQUIVO_BANCO):
        os.remove(ARQUIVO_BANCO)
    criar_tabelas()

    for nome, cidade, estado in CLIENTES:
        cadastrar_cliente(nome, cidade, estado)

    for placa, modelo, capacidade in CAMINHOES:
        cadastrar_caminhao(placa, modelo, capacidade)

    for cliente_id, caminhao_id, peso, saida, prazo in ENTREGAS:
        cadastrar_entrega(cliente_id, caminhao_id, peso, saida, prazo)

    for entrega_id, data in CHEGADAS:
        registrar_chegada(entrega_id, data)


def garantir_banco():
    """Cria o banco com os dados de exemplo só se ele ainda não existir."""
    if not os.path.exists(ARQUIVO_BANCO):
        popular_banco()


if __name__ == "__main__":
    popular_banco()
    print(listar_clientes())
    print(listar_caminhoes())
    print(listar_entregas())