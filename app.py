import streamlit as st
from cadastros import listar_entregas_detalhado

st.set_page_config(page_title="RotaCerta", page_icon="🚚", layout="wide")

st.title("🚚 RotaCerta")
st.write("Sistema de controle de entregas")

st.subheader("Entregas")
st.dataframe(listar_entregas_detalhado())