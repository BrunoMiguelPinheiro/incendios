import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# --- Carregamento dos dados ---
df = pd.read_excel("Incendios_com_Tipologia.xlsx")

# --- Conversão da data e extração do ano ---
df["Data/hora"] = pd.to_datetime(df["Data/hora"])
df["Ano"] = df["Data/hora"].dt.year

# --- Filtros interativos ---
st.sidebar.header("Filtros")

# Ano
anos_disponiveis = sorted(df["Ano"].dropna().unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Tipologia
lista_tipologias = sorted(df["Tipologia"].dropna().unique())
tipologias = st.sidebar.multiselect("Tipologia", lista_tipologias, default=lista_tipologias)

# Freguesia
lista_freguesias = sorted(df["Freguesia"].dropna().unique())
freguesias = st.sidebar.multiselect("Freguesia", lista_freguesias, default=lista_freguesias)

# Parâmetros do Heatmap
st.sidebar.header("Parâmetros do mapa")
raio = st.sidebar.slider("Raio", 1, 50, 15)
blur = st.sidebar.slider("Blur", 1, 50, 10)

# --- Aplicar filtros ---
mask = (
    (df["Ano"].isin(anos_selecionados)) &
    (df["Tipologia"].isin(tipologias)) &
    (df["Freguesia"].isin(freguesias))
)

df_filtrado = df[mask]

# --- Criar mapa ---
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=12)

# Heatmap
heat_data = df_filtrado[["Latitude", "Longitude"]].dropna().values.tolist()
HeatMap(heat_data, radius=raio, blur=blur).add_to(m)

# Marcadores com popups
for _, row in df_filtrado.iterrows():
    popup = f"<b>Tipologia:</b> {row['Tipologia']}<br><b>Data:</b> {row['Data/hora']}<br><b>Local:</b> {row['Localização']}"
    folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=popup).add_to(m)

# --- Mostrar mapa ---
st.title("Mapa de Incêndios por Tipologia")
st.markdown(f"{len(df_filtrado)} ocorrências encontradas.")
st_data = st_folium(m, width=800, height=600)

# --- Exportação ---
st.download_button("📥 Descarregar ficheiro filtrado", data=df_filtrado.to_csv(index=False).encode("utf-8"), file_name="incendios_filtrados.csv", mime="text/csv")
