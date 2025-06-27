import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import gdown
import os

# Google Drive direct download link
# Use the "uc?id=" format instead of "file/d/.../view"
file_id = '17nVHldFwLUca6trQLV-ohrzHDkBr3DK4'
url = f'https://drive.google.com/uc?id={file_id}'

@st.cache_data
def load_data():
    if not os.path.exists("projects.geojson"):
        gdown.download(url, "projects.geojson", quiet=False)
    return gpd.read_file("projects.geojson")

gdf = load_data()

gdf['geometry'] = gdf['geometry'].geometry.simplify(tolerance=0.5, preserve_topology=True)

# User input
project_name_input = st.text_input("Digite o nome do projeto (ou deixe em branco para mostrar todos):")

# Filter
if project_name_input.strip():
    filtered = gdf[gdf["NM_PROJ"].str.contains(project_name_input, case=False, na=False)]
else:
    filtered = gdf

# Map
m = folium.Map(location=[-10, -60], zoom_start=5)
if not filtered.empty:
    folium.GeoJson(
        filtered,
        style_function=lambda x: {'color': 'red', 'weight': 2},
        tooltip=folium.GeoJsonTooltip(fields=['NM_PROJ'], aliases=['AFOLU:'])
    ).add_to(m)
else:
    st.warning("Nenhum projeto encontrado com esse nome.")

# Exemplo: adicionar camadas de Terras Indígenas (se `gdf_ti` estiver definido)
folium.GeoJson(
        data = gdf,
        style_function=lambda x: {'color': 'blue', 'weight': 1, 'fillOpacity': 0},
        tooltip=GeoJsonTooltip(fields=['NM_PROJ'], aliases=['AFOLU:']),
        name="Projetos AFOLU"
    ).add_to(mapa_projetos)


st_folium(m, width=700, height=500)
