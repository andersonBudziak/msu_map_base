import streamlit as st
import geopandas as gpd
import pydeck as pdk
import leafmap.foliumap as leafmap
import streamlit.components.v1 as components

class Tab02:
    
    def __init__(self):
        self.base = 10

    def load_geospatial_data(self, file):
        """Carga datos geoespaciales desde un archivo GeoJSON o KML y retorna un GeoDataFrame."""
        if file.type == 'application/vnd.google-earth.kml+xml':
            # Carga datos KML
            return gpd.read_file(file, driver='KML')
        else:
            # Carga datos GeoJSON
            return gpd.read_file(file)

    def create_map(self, geodata):
        """Crea y muestra un mapa usando pydeck a partir de un GeoDataFrame."""
        # Crea una capa GeoJson para visualización
        layer = pdk.Layer(
            'GeoJsonLayer',
            data=geodata.__geo_interface__,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
        )

        # Configuración de visualización del mapa
        if not geodata.empty:
            view_state = pdk.ViewState(
                latitude=geodata.geometry.centroid.y.mean(),
                longitude=geodata.geometry.centroid.x.mean(),
                zoom=12,
                pitch=50
            )

            # Renderiza el mapa con la capa GeoJson
            st.pydeck_chart(pdk.Deck(
                layers=[layer],
                initial_view_state=view_state
            ))
        else:
            st.error("El archivo no contiene datos de ubicación válidos.")

    def app(self):
        """Crea la interfaz de usuario para cargar un archivo geoespacial y muestra el mapa."""
        # Carga de archivo por parte del usuario
        uploaded_file = st.file_uploader("Elige un archivo con al menos un polígono", type=['geojson', 'kml', 'xml'])
        if uploaded_file is not None:
            # Lee y carga los datos geoespaciales
            geodata = self.load_geospatial_data(uploaded_file)
            # Crea y muestra el mapa
            self.create_map(geodata)

