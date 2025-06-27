import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import gdown
import os

# Google Drive file ID

url = f'https://drive.google.com/file/d/17nVHldFwLUca6trQLV-ohrzHDkBr3DK4/view?usp=sharing'

# Download the file if not already
if not os.path.exists("projects.geojson"):
    gdown.download(url, "projects.geojson", quiet=False)

# Load the GeoJSON
gdf = gpd.read_file("projects.geojson")

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

st_folium(m, width=700, height=500)
