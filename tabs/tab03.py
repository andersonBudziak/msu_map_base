import streamlit as st
import geopandas as gpd
import pydeck as pdk
import leafmap.foliumap as leafmap
import streamlit.components.v1 as components

class Tab03:

    def __init__(self):
        pass

    def app(self):

        base = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Geospatial Analysis Project</title>
                        <style>
                            body { font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; color: #333; }
                            .container { max-width: 800px; margin: 0 auto; padding: 20px; background: white; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); border-radius: 8px; }
                            h1, h2, h3 { color: #642834; }
                            p, li { margin-bottom: 10px; }
                            pre { background: #f4f4f4; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow-x: auto; }
                            code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; color: #642834; }
                            .variables { background: #e3f2fd; padding: 10px; border-left: 5px solid #642834; margin: 20px 0; }
                            .code-section { background: #ffebee; padding: 10px; border-left: 5px solid #642834; margin: 20px 0; }
                            .highlight { color: #642834; font-weight: bold; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>Geospatial Analysis Project</h1>
                            <p>This project involves performing geospatial analysis using Google Earth Engine (GEE) and various custom Python classes for data processing and analysis.</p>
                            
                            <h2>Project Steps</h2>
                            
                            <h3>1. Imports and Initialization</h3>
                            <p>First, we import necessary modules and initialize the Google Earth Engine environment:</p>
                            <div class="code-section">
                                <pre><code>import ee
                    from src.controllers.plotter_base import PhenologyPlotter
                    from src.controllers.metrics_vos_pos import VosPosMetrics
                    from src.controllers.metrics_bos_eso import BosEosMetrics
                    from src.controllers.sentinel_ import Sentinel2Processor
                    from src.controllers.geometry import ProcessadorGeoDataFrame
                    from src.controllers.metrics_geometrics import PhenologyMetrics
                    from src.controllers.time_series import VegetationIndexProcessor

                    # Trigger the authentication flow.
                    ee.Authenticate()

                    # Initialize the library.
                    ee.Initialize(project='ee-carbonei')</code></pre>
                            </div>
                            <p>This sets up the environment for further analysis.</p>

                            <h3>2. Parameters Setup</h3>
                            <p>Next, we define the parameters for our analysis:</p>
                            <div class="variables">
                                <ul>
                                    <li><span class="highlight"><code>start_date</code></span>: The start date for the analysis period. Example: <code>'2022-10-01'</code></li>
                                    <li><span class="highlight"><code>end_date</code></span>: The end date for the analysis period. Example: <code>'2023-04-30'</code></li>
                                    <li><span class="highlight"><code>path</code></span>: The file path to the polygon data. Example: <code>r'data\\ms_field_boundaries.gpkg'</code></li>
                                    <li><span class="highlight"><code>index_poligon</code></span>: The index of the polygon to analyze. Default is 0. Example: <code>3</code></li>
                                    <li><span class="highlight"><code>cloud_probality</code></span>: The threshold for cloud probability to filter images. Example: <code>0.5</code></li>
                                    <li><span class="highlight"><code>vegetation_index</code></span>: The vegetation index to use. Example: <code>'evi_value'</code></li>
                                    <li><span class="highlight"><code>trheasould_index</code></span>: The threshold index value for analysis. Example: <code>2.8</code></li>
                                    <li><span class="highlight"><code>window_size</code></span>: The window size for the Savitzky-Golay filter. Example: <code>30</code></li>
                                    <li><span class="highlight"><code>poly_order</code></span>: The polynomial order for the Savitzky-Golay filter. Example: <code>4</code></li>
                                    <li><span class="highlight"><code>order</code></span>: The order for NDVI processing. Example: <code>20</code></li>
                                </ul>
                            </div>
                            <div class="code-section">
                                <pre><code># Dates of analysis
                    start_date = '2022-10-01'
                    end_date = '2023-04-30'

                    # Path to polygons
                    path = r'data\\ms_field_boundaries.gpkg'

                    # Index of polygon, default is 0
                    index_poligon = 3

                    cloud_probality = 0.5
                    vegetation_index = 'evi_value'
                    trheasould_index = 2.8

                    # Apply Savitzky-Golay filter
                    window_size = 30
                    poly_order = 4

                    # Order NDVI
                    order = 20</code></pre>
                            </div>
                            <p>These parameters are essential for data processing and analysis.</p>
                            
                            <h3>3. Geometry Processing</h3>
                            <p>We read the geometry data and extract coordinates:</p>
                            <div class="code-section">
                                <pre><code># Read geometry file
                    processador = ProcessadorGeoDataFrame(path)
                    vertices, geometry = processador.extrair_coordenadas(index_poligon)

                    # Convert points to a polygon
                    polygon = ee.Geometry.Polygon(vertices)</code></pre>
                            </div>
                            <p>This creates a polygon that will be used in the analysis.</p>

                            <h3>4. Data Processing</h3>
                            <p>We process Sentinel-2 data and apply various analyses:</p>
                            <div class="code-section">
                                <pre><code>s2 = Sentinel2Processor(start_date, end_date, polygon)
                    df = s2.process_data()

                    processor = VegetationIndexProcessor(df, vegetation_index, window_size=7, poly_order=2)
                    df = processor.process()

                    # Get VOS and POS metrics
                    vos_pos_analyzer = VosPosMetrics(df, order)
                    phenology_df = vos_pos_analyzer.analyze_phenology()

                    # Get BOS and EOS metrics
                    analysis = BosEosMetrics(df, phenology_df, trheasould_index)
                    phenology_df = analysis.execute_analysis()

                    analysis_metrics = PhenologyMetrics(phenology_df, df)
                    phenology_df = analysis_metrics.derivate_metrics()</code></pre>
                            </div>
                            <p>This involves processing the data, calculating various metrics, and analyzing phenology.</p>
                            
                            <h2>Conclusion</h2>
                            <p>This project demonstrates a comprehensive approach to geospatial analysis using GEE and Python. The code snippets provided show the main steps involved in data processing and analysis.</p>
                        </div>
                    </body>
                    </html>
                """

        # Display the HTML content in Streamlit
        st.write(base, unsafe_allow_html=True)