
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PhenologyPlotter:
    def __init__(self, df_env, phenology_df, df_index, vegetation_index):
        self.df_env = df_env
        self.phenology_df = phenology_df
        self.vegetation_index = vegetation_index
        self.df_index = df_index

    def convert_dates(self):
        """Convert 'timestamps' and 'Date' in dataframes to datetime objects."""
        self.phenology_df['Date_dt'] = pd.to_datetime(self.phenology_df['Date'])

    def calculate_plot_range(self):
        """Calculate and adjust start and end dates for the plot based on phenology data."""
        vos_start_date = self.phenology_df[self.phenology_df['Phenologic'] == 'vos_start']['Date_dt'].min() - pd.Timedelta(days=3)
        vos_end_date = self.phenology_df[self.phenology_df['Phenologic'] == 'vos_end']['Date_dt'].max() + pd.Timedelta(days=3)
        return vos_start_date, vos_end_date

    def prepare_table(self):
        """Prepare a DataFrame for table visualization."""
        table_df = self.phenology_df[['Date_dt', 'Value', 'Phenologic']].copy()
        table_df['Date_dt'] = table_df['Date_dt'].dt.strftime('%Y-%m-%d').replace(np.nan, '–')
        table_df['Value'] = table_df['Value'].apply(lambda x: f"{x:,.3f}" if isinstance(x, float) else f"{x:,}" if isinstance(x, int) else '-')
        table_df = table_df.rename(columns={'Date_dt': 'Date', 'Value': 'Values', 'Phenologic': 'Phenologic Metrics'})
        return table_df

    def plot_data(self):

        self.convert_dates()
        vos_start_date, vos_end_date = self.calculate_plot_range()
        table_df = self.prepare_table()

        fig = make_subplots(
            rows=1, cols=2,
            shared_xaxes=True,
            horizontal_spacing=0.1,
            specs=[[{"type": "scatter"}, {"type": "table"}]]
        )

        # Cores e outros estilos
        base_color = '#642834'
        other_colors = ['#B19470', '#76453B', '#304D30', '#114232', '#F7F6BB', '#FF9800', '#90D26D']
        background_color = '#FFFFFF'

        # Adicionando traços
        fig.add_trace(go.Scatter(x=self.df_index['timestamps'], y=self.df_index[self.vegetation_index], mode='lines', name='Vegetation Index', line=dict(color=other_colors[3])), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.df_index['timestamps'], y=self.df_index['savitzky_golay'], mode='lines', name='Savitzky-Golay', line=dict(color=base_color, dash='dash')), row=1, col=1)

        for i, metric in enumerate(['vos_start', 'vos_end', 'pos', 'bos_der', 'eos_der', 'bos_abs', 'eos_abs']):
            color = other_colors[i % len(other_colors)]
            metric_df = self.phenology_df[self.phenology_df['Phenologic'] == metric]
            fig.add_trace(go.Scatter(x=metric_df['Date_dt'], y=metric_df['Value'], mode='markers', name=metric, marker=dict(color=color, size=9)), row=1, col=1)

        fig.add_trace(go.Table(
            header=dict(values=['<b>Date</b>', '<b>Values</b>', '<b>Phenologic Metrics</b>'], fill_color=base_color, align='center', font=dict(color='white', size=12)),
            cells=dict(values=[table_df[col] for col in table_df.columns], fill_color=[['lightgrey', 'white'] * len(self.phenology_df)], align='center', font=dict(color='darkslategray', size=11))
        ), row=1, col=2)

        fig.add_annotation(
            text="vos_start: Valley of season, less value before POS",
            xref="paper", yref="paper",
            x=1, y=0.30, showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.add_annotation(
            text="vos_end: Valley of season, less value after",
            xref="paper", yref="paper",
            x=1, y=0.28, showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.add_annotation(
            text="pos: Peak of season",
            xref="paper", yref="paper",
            x=1, y=0.26, showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.add_annotation(
            text="sos_der: Start of season, derivatives",
            xref="paper", yref="paper",
            x=1, y=0.24, showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.add_annotation(
            text="eos_der: End of season, derived",
            xref="paper", yref="paper",
            x=1, y=0.22, showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.add_annotation(
            text="sos_abs: Start of season. Absolute value",
            xref="paper", yref="paper",
            x=1, y=0.20, showarrow=False,
            font=dict(size=12),
            align="center"
        )

        fig.add_annotation(
            text="eos_abs: End of season. Absolute value",
            xref="paper", yref="paper",
            x=1, y=0.18, showarrow=False,
            font=dict(size=12),
            align="right"
        )

        fig.add_trace(go.Scatter(x=list(self.df_index['date_image']), y=list(self.df_index[self.vegetation_index]), mode='markers', name='Base`s images', marker=dict(color='#642834', size=5)), row=1, col=1)

        fig.update_layout(
            height=800,
            width=1200,
            title_text="GCERLab Phenologics Metrics and Expenses",
            xaxis_title="Date",
            yaxis_title="NDVI",
            xaxis_range=[vos_start_date, vos_end_date],
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            legend=dict(
                x=0.01,
                y=0.99,
                font=dict(size=10)
            )
        )

        return fig

    def plot_data_01(self):
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=self.df_index['timestamps'], y=self.df_index['ndvi_value'], name="NDVI"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=self.df_index['timestamps'], y=self.df_index['evi_value'], name="EVI"),
            secondary_y=True,
        )

        fig.add_trace(
            go.Scatter(x=self.df_index['timestamps'], y=self.df_index['savitzky_golay'], name="Savitzky-Golay"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="EVI and NDVI Time Series"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Timestamps")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>NDVI</b> values", secondary_y=False)
        fig.update_yaxes(title_text="<b>EVI</b> values", secondary_y=True)

        return fig
    


    def plot_data_02(self, start_date, end_date):

        """Create and display a Plotly graph with vegetation index and phenology data."""
        self.convert_dates()
        # Colors and other styling
        base_color = '#642834'
        other_colors = ['#B19470', '#76453B', '#304D30', '#114232', '#F7F6BB', '#FF9800', '#90D26D']
        background_color = '#FFFFFF'

        fig = fig = go.Figure()

        # Adding traces
        fig.add_trace(go.Scatter(x=self.df_index['timestamps'], y=self.df_index[self.vegetation_index], mode='lines', name='Vegetation Index', line=dict(color=other_colors[3])))
        fig.add_trace(go.Scatter(x=self.df_index['timestamps'], y=self.df_index['savitzky_golay'], mode='lines', name='Savitzky-Golay', line=dict(color=base_color, dash='dash')))


        fig.add_trace(go.Scatter(x=list(self.df_index['date_image']), y=list(self.df_index[self.vegetation_index]), mode='markers', name='Base images', marker=dict(color='#642834', size=5)))

        fig.update_layout(
            title_text="GCERLab Phenologics Metrics and Expenses",
            xaxis_title="Date",
            yaxis_title="NDVI",
            xaxis_range=[start_date, end_date],
            #plot_bgcolor=background_color,
            #paper_bgcolor=background_color,
            legend=dict(
            x=0.01,
            y=0.99
        )
        )

        return fig

    


