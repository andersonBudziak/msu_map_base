import ee
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


from src.controllers.plotter_base import PhenologyPlotter


class Plots():
        
    def __init__(self) -> None:

        pass

    def plot_precipitation(self, df):


        # Gráfico de barras para a precipitação diária
        fig = px.bar(df, x='date', y='mean_precipitation', title='Sum Daily Precipitation',
                    labels={'date': 'Date', 'mean_precipitation': 'Sum Precipitation (mm)'}, 
                    color_discrete_sequence=['#642834'])

        non_zero_df = df[df['cumulative_precipitation'] != 0]

        # Adicionar o gráfico de linha para a precipitação acumulada usando um segundo eixo Y
        fig.add_trace(
            go.Scatter(x=non_zero_df['date'], y=non_zero_df['cumulative_precipitation'], mode='lines', name='Cumulative Precipitation', 
                    line=dict(color='#304D30'), yaxis='y2')
        )

        # Atualizar o layout para adicionar um segundo eixo Y
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
            legend=dict(
                x=0.01,
                y=0.99
            )
        )

        return fig

    def plot_temperature(self, df):
        
        fig = px.bar(df, x='date', y='temperature_2m_max', title='Max Daily Temperature',
                      labels={'date': 'Date', 'temperature_2m_max': 'Max Temperature (°C)'}, 
                      color_discrete_sequence=['#642834'])
        return fig
    
    def plot_radiation(self, df):

        fig = px.bar(df, x='date', y='surface_net_solar_radiation_sum', title='Surface Net Thermal Radiation',
                      labels={'date': 'Date', 'surface_net_solar_radiation_sum': 'Surface Net Thermal Radiation (J/m²)'}, 
                      color_discrete_sequence=['#642834'])
        return fig
    

    def process_polygon(self, index_poligon):
            
            #Start date analises 
            start_date = '2023-01-01'

            #End date analises
            end_date = '2023-12-30'

            df_enviroents = pd.read_csv(rf"C:\Users\ander\OneDrive\Área de Trabalho\msu\map_base\base\polygon_{index_poligon}\data_base.csv")

            phenology_df = pd.read_csv(rf"C:\Users\ander\OneDrive\Área de Trabalho\msu\map_base\base\polygon_{index_poligon}\phenology_df.csv")

            df_index = pd.read_csv(rf"C:\Users\ander\OneDrive\Área de Trabalho\msu\map_base\base\polygon_{index_poligon}\data_index.csv")

            plotter = PhenologyPlotter(df_enviroents, phenology_df, df_index, 'ndvi_value')
            fig = plotter.plot_data()

            fig_2 = plotter.plot_data_02(start_date, end_date)

            fig_precipitation = self.plot_precipitation(df_enviroents)
            fig_temperature = self.plot_temperature(df_enviroents)
            fig_radiation = self.plot_radiation(df_enviroents)

            return fig_precipitation, fig_temperature, fig_radiation, fig, fig_2


            #fig.show()
            #fig_2.show()

            #   Show the interactive plots
            #fig_precipitation.show()
            #fig_temperature.show()
            #fig_radiation.show()


