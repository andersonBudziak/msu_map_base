import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import streamlit.components.v1 as components

class Tab01:

    def __init__(self):
        self.gdf = gpd.read_file(r'data\farms_.geojson')
        self.lista = list(self.gdf.index)
        self.lista.insert(0, '-')

    def app(self):
        row1_col1, row1_col2 = st.columns([2, 3])

        with row1_col2:
            row1_col2_1, row1_col2_2 = st.columns([1, 3])
            
            with row1_col2_1: 
                lista_escolha = st.selectbox('Select a ID area:', self.lista)
            
            with row1_col2_2:
                st.text('Pass over the polygon to capture its ID,')
                st.text('then select the desired polygon ID to view the area attributes.')

            if lista_escolha != '-':
                HtmlFile = open(rf"htmls\{str(lista_escolha)}.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read()
                components.html(source_code, height=600)

        with row1_col1:
            m = leafmap.Map()
            m.add_xyz_service('xyz.Esri.WorldImagery')
            m.add_gdf(self.gdf, layer_name='Farms', label='index')

            if lista_escolha != '-':
                selected_polygon = self.gdf.loc[int(lista_escolha)]
                minx, miny, maxx, maxy = selected_polygon.geometry.bounds
                m.fit_bounds([[miny, minx], [maxy, maxx]])

            m.to_streamlit(height=700)