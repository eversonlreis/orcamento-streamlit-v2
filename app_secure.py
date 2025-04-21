
import streamlit as st
import pandas as pd
import json
import gspread
from google.oauth2 import service_account
from gspread_dataframe import set_with_dataframe

st.set_page_config(page_title="Módulo 1 - Orçamento", layout="wide")
st.title("📊 Módulo 1: Parâmetros Iniciais (Google Sheets via segredo)")

# Lendo a credencial do segredo armazenado no Streamlit Cloud
servico_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])

# Autenticar com Google Sheets
credenciais = service_account.Credentials.from_service_account_info(
    servico_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# ID da planilha no Google Sheets (ajuste se necessário)
sheet_id = "1aUzealEj-M7RVc4XPoVzTkLM7e7UTRvmFusx-BMwLfY"
gs = gspread.authorize(credenciais)
sh = gs.open_by_key(sheet_id)
worksheet = sh.worksheet("Dados")

# Lendo dados existentes
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("1. Dados Existentes na Planilha")
st.dataframe(df)

st.subheader("2. Adicionar Novo Registro")
with st.form("form_novo_registro"):
    unidade = st.text_input("Unidade de Negócio")
    responsavel = st.text_input("Responsável")
    ano = st.number_input("Ano", value=2025, step=1)
    mes = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    enviado = st.form_submit_button("Adicionar")

    if enviado:
        novo_id = df["ID"].max() + 1 if not df.empty else 1
        novo_registro = pd.DataFrame([{
            "ID": novo_id,
            "Unidade de Negócio": unidade,
            "Responsável": responsavel,
            "Ano": ano,
            "Mês": mes
        }])
        df = pd.concat([df, novo_registro], ignore_index=True)

        worksheet.clear()
        set_with_dataframe(worksheet, df)

        st.success("Registro salvo no Google Sheets com sucesso!")
        st.dataframe(df)
