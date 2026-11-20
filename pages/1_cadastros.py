from datetime import date

import pandas as pd
import streamlit as st

from cadastros import (
    listar_clientes, listar_caminhoes, listar_entregas_detalhado,
    cadastrar_entrega, registrar_chegada,
)

st.set_page_config(page_title="Cadastros | RotaCerta", page_icon="🚚", layout="wide")
st.title("📝 Cadastros")

col_esq, col_dir = st.columns(2)

# ---------- Nova entrega ----------

with col_esq:
    st.subheader("Nova entrega")

    clientes = listar_clientes()
    caminhoes = listar_caminhoes()

    nomes_clientes = dict(zip(clientes["id"], clientes["nome"]))
    placas = dict(zip(caminhoes["id"], caminhoes["placa"] + " – " + caminhoes["modelo"]))
    capacidades = dict(zip(caminhoes["id"], caminhoes["capacidade_kg"]))

    with st.form("nova_entrega", clear_on_submit=False):
        cliente_id = st.selectbox("Cliente", clientes["id"], format_func=nomes_clientes.get)
        caminhao_id = st.selectbox("Caminhão", caminhoes["id"], format_func=placas.get)
        peso = st.number_input("Peso (kg)", min_value=1, step=100)
        saida = st.date_input("Data de saída", value=date.today(), format="DD/MM/YYYY")
        prazo = st.date_input("Prazo", value=date.today(), format="DD/MM/YYYY")
        enviar = st.form_submit_button("Cadastrar entrega")

    if enviar:
        if peso > capacidades[caminhao_id]:
            st.error(f"Esse caminhão aguenta no máximo {capacidades[caminhao_id]:.0f} kg.")
        elif prazo < saida:
            st.error("O prazo não pode ser antes da data de saída.")
        else:
            cadastrar_entrega(int(cliente_id), int(caminhao_id), peso,
                              saida.isoformat(), prazo.isoformat())
            st.success("Entrega cadastrada!")

# ---------- Registrar chegada ----------

with col_dir:
    st.subheader("Registrar chegada")

    entregas = listar_entregas_detalhado()
    pendentes = entregas[entregas["data_entrega"].isna()]

    if pendentes.empty:
        st.info("Nenhuma entrega em rota. 🎉")
    else:
        descricoes = dict(zip(
            pendentes["id"],
            "Nº " + pendentes["id"].astype(str) + " – " + pendentes["cliente"],
        ))

        with st.form("chegada"):
            entrega_id = st.selectbox("Entrega", pendentes["id"], format_func=descricoes.get)
            chegada = st.date_input("Data de chegada", value=date.today(), format="DD/MM/YYYY")
            confirmar = st.form_submit_button("Registrar chegada")

        if confirmar:
            registrar_chegada(int(entrega_id), chegada.isoformat())
            st.success("Chegada registrada!")
            st.rerun()