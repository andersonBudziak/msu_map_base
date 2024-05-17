import streamlit as st
import geopandas as gpd
import pydeck as pdk

from tabs.tab01 import Tab01
from tabs.tab02 import Tab02

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["Farms MSU", "Metrics by Polygon", "Metrics explantion"])

tab01 = Tab01()
tab02 = Tab02()

with tab1:
    tab01.app()

with tab2:
    tab02.app()

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")
