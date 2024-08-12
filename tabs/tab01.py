import json
import folium as fl
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import st_folium
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from src.managers.plots import Plots

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

        # Normalize area values to use in color scaling
        min_area = self.gdf['area'].min()
        max_area = self.gdf['area'].max()
        self.gdf['normalized_area'] = (self.gdf['area'] - min_area) / (max_area - min_area)

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

        # Função para criar uma cor a partir de uma interpolação entre duas cores hexadecimais
        def interpolate_color(val, min_val, max_val, start_color, end_color):
            ratio = (val - min_val) / (max_val - min_val)
            return (
                int(start_color[1:3], 16) * (1 - ratio) + int(end_color[1:3], 16) * ratio,
                int(start_color[3:5], 16) * (1 - ratio) + int(end_color[3:5], 16) * ratio,
                int(start_color[5:7], 16) * (1 - ratio) + int(end_color[5:7], 16) * ratio
            )

        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

        # Cores de início e fim
        start_color = "#96B5F7"  # Amarelo claro
        end_color = "#FF0000"    # Vermelho escuro

        # Função para estilizar cada polígono com base na área
        def style_function(feature):
            area = feature['properties']['area']
            fill_color = rgb_to_hex(interpolate_color(area, min_area, max_area, start_color, end_color))
            return {
                'fillColor': fill_color,
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.7
            }

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

        fl.GeoJson(self.gdf, style_function=style_function, tooltip=tooltip).add_to(m)

        fl.LayerControl().add_to(m)

        map = st_folium(m, height=900, width=1750)

        # Obter a posição clicada no mapa
        if 'last_clicked' in map and map['last_clicked']:
            data = self.get_pos(map['last_clicked']['lat'], map['last_clicked']['lng'])
            if data is not None:

                # Cria um ponto a partir da coordenada
                point = Point(map['last_clicked']['lng'], map['last_clicked']['lat'])

                # Seleciona o polígono que contém o ponto
                selected_polygon = self.gdf[self.gdf.contains(point)]

                polygon_id = selected_polygon['id'].iloc[0]

                st.title(f'Metrics from {polygon_id} plotland')

                fig_precipitation, fig_temperature, fig_radiation, fig, fig_2, fig_index  = self.plot.process_polygon(selected_polygon['id'].iloc[0])

                st.plotly_chart(fig, use_container_width=True)
                #st.plotly_chart(fig_2, use_container_width=True)
                st.plotly_chart(fig_index, use_container_width=True)
                st.plotly_chart(fig_precipitation, use_container_width=True)
                st.plotly_chart(fig_temperature, use_container_width=True)
                st.plotly_chart(fig_radiation, use_container_width=True)
