
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from gspread_dataframe import set_with_dataframe

st.set_page_config(page_title="Módulo 1 - Parâmetros Iniciais", layout="wide")

st.title("📊 Módulo 1: Parâmetros Iniciais (com Google Sheets)")

# Autenticação com Google Sheets via conta de serviço
credenciais = service_account.Credentials.from_service_account_file(
    "credenciais_gsheet_everson.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# ID da planilha do Google Sheets (substitua se for diferente)
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
