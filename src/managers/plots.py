import os
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.colors import to_hex
from plotly.subplots import make_subplots

from src.controllers.plotter_base import PhenologyPlotter

class Plots():
        
    def __init__(self) -> None:

        pass

    def plot_precipitation(self, df):

        fig = px.bar(df, x='date', y='mean_precipitation', title='Sum Daily Precipitation',
                    labels={'date': 'Date', 'mean_precipitation': 'Sum Precipitation (mm)'}, 
                    color_discrete_sequence=['#642834'])

        non_zero_df = df[df['cumulative_precipitation'] != 0]

        fig.add_trace(
            go.Scatter(x=non_zero_df['date'], y=non_zero_df['cumulative_precipitation'], mode='lines', name='Cumulative Precipitation', 
                    line=dict(color='#304D30'), yaxis='y2')
        )

        fig.update_layout(
            yaxis=dict(
                title='Sum Precipitation (mm)',
                titlefont=dict(color='black'),
                tickfont=dict(color='black')
            ),
            yaxis2=dict(
                title='Cumulative Precipitation (mm)',
                titlefont=dict(color='black'),
                tickfont=dict(color='black'),
                overlaying='y',
                side='right'
            ),

        )

        return fig

    def plot_temperature(self, df):

        # Criando o gráfico
        fig = go.Figure()

        # Adicionando a faixa de variação
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temperature_2m_max'],
            mode='lines',
            showlegend=True,
            name='Max',
            line=dict(color='red')
        ))

                # Adicionando a linha da média
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=(df['temperature_2m_max']+df['temperature_2m_min'])/2,
            mode='lines',
            name='Mean',
            line=dict(color='rgba(100, 40, 52, 1)')
        ))


        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temperature_2m_min'],
            mode='lines',
            showlegend=True,
            name='Min',
            line=dict(color='blue')
        ))


        # Configurações do layout
        fig.update_layout(
            title='Daily Temperature Ranges',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
                        legend=dict(
                x=0.01,
                y=0.99
            ),
        )

        return fig

    def plot_radiation(self, df):

        fig = px.bar(df, x='date', y='surface_net_solar_radiation_sum', title='Surface Net Thermal Radiation',
                      labels={'date': 'Date', 'surface_net_solar_radiation_sum': 'Surface Net Thermal Radiation (J/m²)'}, 
                      color_discrete_sequence=['#642834'])
        return fig
    
    def index_acumulated(self, df):

            data = df
            # Converter a coluna 'date_image' para datetime
            data['date_image'] = pd.to_datetime(data['date_image'])

            # Adicionar uma coluna para o dia do ano
            data['day_of_year'] = data['date_image'].dt.dayofyear

            # Obter os anos únicos no dataset
            anos = data['date_image'].dt.year.unique()

            # Criar a paleta de cores baseada na cor #642834
            num_colors = len(anos)

            colors = [to_hex(c) for c in cm.viridis(np.linspace(0, 1, num_colors))]

            # Criar o gráfico interativo com uma linha para cada ano
            fig = make_subplots()

            for i, ano in enumerate(anos):
                dados_ano = data[data['date_image'].dt.year == ano]
                fig.add_trace(go.Scatter(
                    x=dados_ano['day_of_year'],
                    y=dados_ano['ndvi_value'],
                    mode='lines+markers',
                    name=str(ano),
                    line=dict(color=colors[i])
                ))

                fig.update_layout(
                    title_text="GCERLab NDVI time series",
                    xaxis_title="Date",
                    yaxis_title="NDVI",
                    #plot_bgcolor=background_color,
                    #paper_bgcolor=background_color,
                    legend=dict(
                    x=0.01,
                    y=0.99
                )
                )

            return fig
                

    def process_polygon(self, index_poligon):
            
            start_date = '2023-01-01'

            end_date = '2023-12-30'

            df_enviroents = pd.read_csv(rf"base/polygon_{index_poligon}/data_base.csv")

            phenology_df = pd.read_csv(rf"base/polygon_{index_poligon}/phenology_df.csv")

            df_index = pd.read_csv(rf"base/polygon_{index_poligon}/data_index.csv")
            
            df_s2 = pd.read_csv(rf"base/polygon_{index_poligon}/data_s2.csv")

            plotter = PhenologyPlotter(df_enviroents, phenology_df, df_index, 'ndvi_value')
            fig = plotter.plot_data()

            fig_2 = plotter.plot_data_02(start_date, end_date)

            fig_precipitation = self.plot_precipitation(df_enviroents)
            fig_temperature = self.plot_temperature(df_enviroents)
            fig_radiation = self.plot_radiation(df_enviroents)
            fig_index = self.index_acumulated(df_s2)

            return fig_precipitation, fig_temperature, fig_radiation, fig, fig_2, fig_index

