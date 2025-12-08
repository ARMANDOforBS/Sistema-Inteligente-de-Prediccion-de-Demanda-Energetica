import streamlit as st
import pandas as pd
import os
from datetime import datetime

from src.data_loader import load_data, clean_data, enrich_data_with_users
from src.weather_service import WeatherService
from src.predictor import EnergyPredictor
from src.visualizer import EnergyVisualizer
from src.ui_styles import get_custom_css

st.set_page_config(
    page_title="Predicción Energética Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

def main():
    st.title("Sistema Inteligente de Predicción Energética")
    st.markdown("<p style='margin-top: -15px; font-size: 1.1rem; color: #8b949e;'>Dashboard Interactivo Multiparadigma</p>", unsafe_allow_html=True)

    st.markdown("---")
    
    with st.sidebar:
        st.header("Configuración")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("1. Origen de Datos")
        
        if 'active_df' not in st.session_state:
            st.session_state.active_df = None
        if 'active_filename' not in st.session_state:
            st.session_state.active_filename = None

        if st.session_state.active_df is None:
            uploaded_file = st.file_uploader("Arrastra tu CSV aquí", type=["csv"], help="Asegúrate que tenga columnas: Fecha, Usuario, etc.")
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.active_df = df
                    st.session_state.active_filename = uploaded_file.name
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")
        else:
            col_text, col_close = st.columns([0.85, 0.15], vertical_alignment="center")
            with col_text:
                st.markdown(f"""
                    <div style="display: flex; align-items: center; height: 100%;">
                        <span style="font-size: 1rem; color: #e6edf3;">📄 {st.session_state.active_filename}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col_close:
                if st.button("✕", help="Eliminar archivo", key="remove_file_btn"):
                    st.session_state.active_df = None
                    st.session_state.active_filename = None
                    st.rerun()
        
        st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)
        
        st.subheader("2. Datos Climáticos")
        
        CITIES = {
            "Lima, Perú": (-12.0464, -77.0428),
            "Arequipa, Perú": (-16.4090, -71.5375),
            "Cusco, Perú": (-13.5320, -71.9675),
            "Trujillo, Perú": (-8.1091, -79.0215),
            "Madrid, España": (40.4168, -3.7038),
            "Barcelona, España": (41.3851, 2.1734),
            "Ciudad de México, México": (19.4326, -99.1332),
            "Monterrey, México": (25.6866, -100.3161),
            "Bogotá, Colombia": (4.7110, -74.0721),
            "Medellín, Colombia": (6.2442, -75.5812),
            "Buenos Aires, Argentina": (-34.6037, -58.3816),
            "Córdoba, Argentina": (-31.4201, -64.1888),
            "Santiago, Chile": (-33.4489, -70.6693),
            "New York, USA": (40.7128, -74.0060),
            "Los Angeles, USA": (34.0522, -118.2437),
            "Chicago, USA": (41.8781, -87.6298),
            "Miami, USA": (25.7617, -80.1918),
            "London, UK": (51.5074, -0.1278),
            "Paris, Francia": (48.8566, 2.3522),
            "Berlin, Alemania": (52.5200, 13.4050),
            "Rome, Italia": (41.9028, 12.4964),
            "Tokyo, Japón": (35.6762, 139.6503),
            "Seoul, Corea del Sur": (37.5665, 126.9780),
            "Beijing, China": (39.9042, 116.4074),
            "Sao Paulo, Brasil": (-23.5505, -46.6333),
            "Rio de Janeiro, Brasil": (-22.9068, -43.1729),
            "Sydney, Australia": (-33.8688, 151.2093),
            "Quito, Ecuador": (-0.1807, -78.4678),
            "Caracas, Venezuela": (10.4806, -66.9036),
            "La Paz, Bolivia": (-16.5000, -68.1193),
            "Montevideo, Uruguay": (-34.9011, -56.1645),
            "Asunción, Paraguay": (-25.2637, -57.5759),
            "Toronto, Canadá": (43.6532, -79.3832),
            "Dubai, EAU": (25.2769, 55.2962),
            "Moscow, Rusia": (55.7558, 37.6173)
        }
        
        selected_city = st.selectbox(
            "Seleccionar Ciudad", 
            options=sorted(CITIES.keys()), 
            index=sorted(CITIES.keys()).index("Lima, Perú"),
            help="Al cambiar la ciudad, el sistema descarga nuevos datos climáticos (temperatura, radiación) para esa ubicación y re-entrena el modelo IA. Esto ajusta las predicciones al clima local."
        )
        
        lat, lon = CITIES[selected_city]
        
        st.caption(f"Coordenadas activas: {lat:.4f}, {lon:.4f}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        run_btn = st.button("Iniciar Predicción")

    if run_btn:
        with st.spinner('Procesando datos...'):
            if st.session_state.active_df is not None:
                raw_df = st.session_state.active_df
            elif os.path.exists('data/enunciado1_energia.csv'):
                raw_df = load_data('data/enunciado1_energia.csv')
            else:
                st.error("No hay datos disponibles.")
                return

            clean_df = clean_data(raw_df)
            
            start_date = clean_df['Fecha'].min().strftime('%Y-%m-%d')
            end_date = clean_df['Fecha'].max().strftime('%Y-%m-%d')
            
            weather_service = WeatherService(lat=lat, lon=lon)
            try:
                weather_data = weather_service.fetch_historical_weather(start_date, end_date)
                if not weather_data.empty:
                    final_df = pd.merge(clean_df, weather_data, on='Fecha', how='left')
                    final_df = final_df.ffill().bfill()
                else:
                    st.toast("API sin respuesta. Usando datos internos.")
                    final_df = clean_df
            except Exception:
                final_df = clean_df

            final_df = enrich_data_with_users(final_df)
            predictor = EnergyPredictor()
            X, y = predictor.prepare_data(final_df)
            X_test, y_test, y_pred = predictor.train(X, y)
            
            visualizer = EnergyVisualizer()
            
            from sklearn.metrics import mean_squared_error, r2_score
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            rmse = mse ** 0.5

            st.markdown("### Métricas de Inteligencia Artificial")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(
                    "Precisión (R2 Score)", 
                    f"{r2:.2f}", 
                    delta="vs Modelo Base",
                    help="Coeficiente de determinación. Indica qué tan bien el modelo predice el consumo real (1.00 es perfecto)."
                )
            with kpi2:
                st.metric(
                    "Error MSE", 
                    f"{int(mse)}", 
                    delta=f"RMSE: ± {int(rmse)} kWh",
                    help=f"MSE: {int(mse)}. RMSE (Raíz del Error): +/- {int(rmse)} kWh. Indica cuánto se equivoca el modelo en promedio."
                )
            with kpi3:
                st.metric(
                    "Datos Analizados", 
                    f"{len(final_df)}", 
                    delta="Total Histórico",
                    help="Cantidad total de registros procesados (filas) del dataset histórico + enriquecimiento."
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("### Visualización de Demandas")
            tab_main, tab_dist, tab_valid, tab_map = st.tabs(["Línea de Tiempo", "Distribución Global", "Validación IA", "Mapa Geográfico"])
            
            with tab_main:
                fig_trend = visualizer.plot_consumption_trend_interactive(final_df)
                st.plotly_chart(fig_trend, use_container_width=True)
                
            with tab_dist:
                fig_bar = visualizer.plot_user_distribution_interactive(final_df)
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with tab_valid:
                df_pred = pd.DataFrame({'Real': y_test, 'Predicho': y_pred})
                fig_scatter = visualizer.plot_prediction_validation_interactive(df_pred)
                st.plotly_chart(fig_scatter, use_container_width=True)
                
            with tab_map:
                st.markdown("#### Ubicación de la Fuente de Datos")
                df_map = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                st.map(df_map, zoom=6, use_container_width=True)
                st.info(f"Visualizando datos para: **{selected_city}**")

            st.markdown("---")
            st.caption(f"Sistema generado automáticamante | Ejecución: {datetime.now().strftime('%H:%M:%S')}")

    else:
        st.markdown(
            """
            <div style='text-align: center; padding: 50px; color: #8b949e;'>
                <h3>Esperando orden de ejecución</h3>
                <p>Configura los parámetros en el panel lateral y presiona <b>Iniciar Predicción</b>.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
