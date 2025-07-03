import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
from streamlit_folium import st_folium

# Título da aplicação
st.title("Incêndios por Ano, Tipologia e Freguesia")

# Carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Incendios_com_Tipologia.xlsx")
    df["Data/hora"] = pd.to_datetime(df["Data/hora"])
    df["Ano"] = df["Data/hora"].dt.year
    df["Mês"] = df["Data/hora"].dt.month_name()
    return df

df = carregar_dados()

# Filtros
anos = sorted(df["Ano"].unique())
tipologias = sorted(df["Tipologia"].dropna().unique())
freguesias = sorted(df["Freguesia"].dropna().unique())

ano_escolhido = st.selectbox("Seleciona o Ano", anos)
tipologia_escolhida = st.selectbox("Seleciona a Tipologia", tipologias)
freguesia_escolhida = st.selectbox("Seleciona a Freguesia (opcional)", ["Todas"] + freguesias)

meses_disponiveis = sorted(df[df["Ano"] == ano_escolhido]["Mês"].unique())
mes_escolhido = st.selectbox("Seleciona o Mês (opcional)", ["Todos"] + meses_disponiveis)

# Filtrar os dados
df_filtrado = df[(df["Ano"] == ano_escolhido) & (df["Tipologia"] == tipologia_escolhida)]
if freguesia_escolhida != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Freguesia"] == freguesia_escolhida]
if mes_escolhido != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Mês"] == mes_escolhido]

# Gerar mapa
if df_filtrado.empty:
    st.warning("Não existem dados para os filtros selecionados.")
else:
    m = folium.Map(location=[df_filtrado["Latitude"].mean(), df_filtrado["Longitude"].mean()], zoom_start=11)
    pontos = df_filtrado[["Latitude", "Longitude"]].dropna().values.tolist()
    HeatMap(pontos, radius=10, blur=15).add_to(m)
    st_folium(m, width=700, height=500)

    # Exportar ficheiro filtrado
    st.download_button(
        "📥 Descarregar ficheiro filtrado",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="incendios_filtrados.csv",
        mime="text/csv"
    )
