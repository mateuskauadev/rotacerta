from datetime import date

import pandas as pd
import streamlit as st
import io

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

# ---------- Filtros (menu lateral) ----------

st.sidebar.header("Filtros")
filtro_status = st.sidebar.multiselect("Status", sorted(entregas["status"].unique()))
filtro_cliente = st.sidebar.multiselect("Cliente", sorted(entregas["cliente"].unique()))
filtro_caminhao = st.sidebar.multiselect("Caminhão", sorted(entregas["caminhao"].unique()))

filtradas = entregas
if filtro_status:
    filtradas = filtradas[filtradas["status"].isin(filtro_status)]
if filtro_cliente:
    filtradas = filtradas[filtradas["cliente"].isin(filtro_cliente)]
if filtro_caminhao:
    filtradas = filtradas[filtradas["caminhao"].isin(filtro_caminhao)]

# ---------- Indicadores ----------

total = len(filtradas)
no_prazo = filtradas["status"].str.contains("No prazo").sum()
atrasadas = (filtradas["status"] == "🔴 Atrasada").sum()
em_rota = filtradas["status"].str.contains("Em rota").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de entregas", total)
col2.metric("No prazo", no_prazo)
col3.metric("Atrasadas", atrasadas)
col4.metric("Em rota", em_rota)

# ---------- Gráficos ----------

graf1, graf2 = st.columns(2)

por_status = filtradas["status"].value_counts()
graf1.subheader("Entregas por status")
graf1.bar_chart(por_status)

so_atrasadas = filtradas[filtradas["status"].str.contains("Atrasada")]
por_cliente = so_atrasadas["cliente"].value_counts()
graf2.subheader("Atrasos por cliente")
graf2.bar_chart(por_cliente)

# ---------- Tabela ----------

st.subheader("Entregas")

tabela = filtradas.copy()
for coluna in ["data_saida", "prazo", "data_entrega"]:
    tabela[coluna] = pd.to_datetime(tabela[coluna])

st.dataframe(
    tabela,
    hide_index=True,
    column_order=["id", "status", "cliente", "caminhao", "peso_kg",
                  "data_saida", "prazo", "data_entrega"],
    column_config={
        "id": st.column_config.NumberColumn("Nº", format="%d"),
        "status": "Status",
        "cliente": "Cliente",
        "caminhao": "Caminhão",
        "peso_kg": st.column_config.NumberColumn("Peso", format="%d kg"),
        "data_saida": st.column_config.DateColumn("Saída", format="DD/MM/YYYY"),
        "prazo": st.column_config.DateColumn("Prazo", format="DD/MM/YYYY"),
        "data_entrega": st.column_config.DateColumn("Entregue em", format="DD/MM/YYYY"),
    },
)
# ---------- Exportar ----------

exportar = filtradas[["id", "status", "cliente", "caminhao", "peso_kg",
                      "data_saida", "prazo", "data_entrega"]].rename(columns={
    "id": "Nº", "status": "Status", "cliente": "Cliente", "caminhao": "Caminhão",
    "peso_kg": "Peso (kg)", "data_saida": "Saída", "prazo": "Prazo",
    "data_entrega": "Entregue em",
})

arquivo = io.BytesIO()
exportar.to_excel(arquivo, index=False, sheet_name="Entregas")

st.download_button(
    "📥 Exportar para Excel",
    data=arquivo.getvalue(),
    file_name=f"rotacerta_entregas_{date.today().isoformat()}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)