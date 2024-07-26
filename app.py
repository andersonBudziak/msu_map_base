import streamlit as st

from tabs.tab01 import Tab01
from tabs.tab02 import Tab02
from tabs.tab03 import Tab03

# Configurar o layout da página para tela cheia
st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["Mississippi Boundaries Farms", "Metrics by Polygon", "Metrics explantion"])

tab01 = Tab01()
tab02 = Tab02()
tab03 = Tab03()

with tab1:
    tab01.app()

with tab2:
    tab02.app()

with tab3:
    tab03.app()
