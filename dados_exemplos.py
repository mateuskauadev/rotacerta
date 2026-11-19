import os
from banco import criar_tabelas
from cadastros import (
    cadastrar_cliente, listar_clientes,
    cadastrar_caminhao, listar_caminhoes,
    cadastrar_entrega, listar_entregas,
    registrar_chegada,
)

# 1. Começar do zero: apaga o banco antigo (se existir) e cria as tabelas vazias
if os.path.exists("rotacerta.db"):
    os.remove("rotacerta.db")
criar_tabelas()

# 2. Clientes: (nome, cidade, estado)
clientes = [
    ("Mercado Bom Preço", "Rio de Janeiro", "RJ"),
    ("Supermercado Guanabara", "Rio de Janeiro", "RJ"),
    ("Drogaria Vida Leve", "Niterói", "RJ"),
    ("Atacadão Paulista", "São Paulo", "SP"),
    ("Casa do Construtor Minas", "Belo Horizonte", "MG"),
    ("Hortifruti Serra Verde", "Petrópolis", "RJ"),
]
for nome, cidade, estado in clientes:
    cadastrar_cliente(nome, cidade, estado)

# 3. Caminhões: (placa, modelo, capacidade_kg)
caminhoes = [
    ("RIO1A23", "Volvo FH 540", 25000),
    ("KXP2B45", "Mercedes Atego 2430", 14000),
    ("LTN3C67", "VW Delivery 11.180", 8000),
    ("QRS4D89", "Iveco Daily 35-150", 3500),
]
for placa, modelo, capacidade in caminhoes:
    cadastrar_caminhao(placa, modelo, capacidade)

# 4. Entregas: (cliente_id, caminhao_id, peso_kg, data_saida, prazo)
entregas = [
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
for cliente_id, caminhao_id, peso, saida, prazo in entregas:
    cadastrar_entrega(cliente_id, caminhao_id, peso, saida, prazo)

# 5. Chegadas: (entrega_id, data_entrega). As entregas 11 a 14 ainda estão em rota.
chegadas = [
    (1, "2026-11-05"),   # no prazo
    (2, "2026-11-08"),   # atrasada
    (3, "2026-11-06"),   # no prazo
    (4, "2026-11-09"),   # adiantada
    (5, "2026-11-13"),   # atrasada
    (6, "2026-11-10"),   # no prazo
    (7, "2026-11-12"),   # no prazo
    (8, "2026-11-17"),   # atrasada
    (9, "2026-11-14"),   # no prazo
    (10, "2026-11-18"),  # atrasada
]
for entrega_id, data in chegadas:
    registrar_chegada(entrega_id, data)

# 6. Conferir
print(listar_clientes())
print(listar_caminhoes())
print(listar_entregas())