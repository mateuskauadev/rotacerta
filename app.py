from datetime import date

import pandas as pd
import streamlit as st

from cadastros import listar_entregas_detalhado

st.set_page_config(page_title="RotaCerta", page_icon="🚚", layout="wide")


# ---------- Regras de status ----------

def status_chegada(data_entrega, prazo):
    if data_entrega > prazo:
        return "🔴 Atrasada"
    else:
        return "🟢 No prazo"


def status_em_rota(hoje, prazo):
    if hoje > prazo:
        return "🟠 Em rota (atrasada)"
    else:
        return "🟡 Em rota"


def definir_status(linha):
    hoje = date.today().isoformat()

    if pd.isna(linha["data_entrega"]):
        return status_em_rota(hoje, linha["prazo"])
    else:
        return status_chegada(linha["data_entrega"], linha["prazo"])


# ---------- Página ----------

st.title("🚚 RotaCerta")
st.write("Sistema de controle de entregas")

entregas = listar_entregas_detalhado()
entregas["status"] = entregas.apply(definir_status, axis=1)

total = len(entregas)
no_prazo = entregas["status"].str.contains("No prazo").sum()
atrasadas = (entregas["status"] == "🔴 Atrasada").sum()
em_rota = entregas["status"].str.contains("Em rota").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de entregas", total)
col2.metric("No prazo", no_prazo)
col3.metric("Atrasadas", atrasadas)
col4.metric("Em rota", em_rota)

st.subheader("Entregas")
st.dataframe(entregas, hide_index=True)