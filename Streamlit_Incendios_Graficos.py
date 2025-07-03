import streamlit as st
import pandas as pd
import plotly.express as px

# Título
st.title("Gráficos de Ocorrências de Incêndios")

# Carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Incendios_com_Tipologia.xlsx")
    df["Data/hora"] = pd.to_datetime(df["Data/hora"])
    df["Ano"] = df["Data/hora"].dt.year
    df["Mês"] = df["Data/hora"].dt.month_name()
    return df

df = carregar_dados()

# Filtros laterais
with st.sidebar:
    st.header("Filtros")
    anos = sorted(df["Ano"].unique())
    ano_escolhido = st.selectbox("Seleciona o Ano", anos)
    tipologias = sorted(df["Tipologia"].dropna().unique())
    tipologia_escolhida = st.selectbox("Seleciona a Tipologia", ["Todas"] + tipologias)

# Aplicar filtros
df_filtrado = df[df["Ano"] == ano_escolhido]
if tipologia_escolhida != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Tipologia"] == tipologia_escolhida]

# Gráfico por Freguesia
st.subheader("Número de Ocorrências por Freguesia")
df_freguesia = df_filtrado["Freguesia"].value_counts().reset_index()
df_freguesia.columns = ["Freguesia", "Ocorrências"]
fig_freguesia = px.bar(df_freguesia, x="Freguesia", y="Ocorrências", color="Ocorrências", title="Ocorrências por Freguesia")
st.plotly_chart(fig_freguesia)

# Gráfico por Mês
st.subheader("Número de Ocorrências por Mês")
df_mes = df_filtrado["Mês"].value_counts().reindex(
    ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
).dropna().reset_index()
df_mes.columns = ["Mês", "Ocorrências"]
fig_mes = px.bar(df_mes, x="Mês", y="Ocorrências", color="Ocorrências", title="Ocorrências por Mês")
st.plotly_chart(fig_mes)