import json
import folium as fl
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import st_folium

from src.managers.plots import Plots

# Configurar o layout da página para tela cheia
#st.set_page_config(layout="wide")

class Tab01:

    def __init__(self):

        self.plot = Plots()

                # Caminho para o arquivo GPKG
        gpkg_path = "ms_field_boundaries.gpkg"  # Substitua pelo caminho do seu arquivo GPKG

        # Carregar o arquivo GPKG usando geopandas
        gdf = gpd.read_file(gpkg_path)

        self.gdf = gdf.to_crs('EPSG:4326')

    # Função para obter a posição clicada no mapa
    def get_pos(self, lat, lng):
        return lat, lng

    def app(self):


        # Calcular o bounding box
        minx = self.gdf.dissolve().bounds.loc[0].minx 
        miny = self.gdf.dissolve().bounds.loc[0].miny 
        maxx = self.gdf.dissolve().bounds.loc[0].maxx 
        maxy = self.gdf.dissolve().bounds.loc[0].maxy

        # Criar o mapa Folium centrado no bounding box
        m = fl.Map(
            location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=13
        )

        fl.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = True,
                control = True
            ).add_to(m)

        tooltip = fl.GeoJsonTooltip(
            fields=["id", "tile"],
            aliases=["Polygon ID:", "Tile identification:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """
        )

        fl.GeoJson(self.gdf, tooltip=tooltip).add_to(m)

        # Adicionar um popup para obter coordenadas ao clicar no mapa
        #m.add_child(fl.LatLngPopup())

        # Exibir o mapa em tela cheia no Streamlit
        map = st_folium(m, height=900, width=1800)

        # Obter a posição clicada no mapa
        if 'last_clicked' in map and map['last_clicked']:
            data = self.get_pos(map['last_clicked']['lat'], map['last_clicked']['lng'])
            if data is not None:

                # Cria um ponto a partir da coordenada
                point = Point(map['last_clicked']['lng'], map['last_clicked']['lat'])

                # Seleciona o polígono que contém o ponto
                selected_polygon = self.gdf[self.gdf.contains(point)]

                polygon_id = selected_polygon['id'].iloc[0]

                st.title(f'Metrics from {polygon_id} polygon')

                fig_precipitation, fig_temperature, fig_radiation, fig, fig_2  = self.plot.process_polygon(selected_polygon['id'].iloc[0])

                st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig_2, use_container_width=True)
                st.plotly_chart(fig_precipitation, use_container_width=True)
                st.plotly_chart(fig_temperature, use_container_width=True)
                st.plotly_chart(fig_radiation, use_container_width=True)