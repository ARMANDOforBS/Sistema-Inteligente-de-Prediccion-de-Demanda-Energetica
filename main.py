import os
import sys
import pandas as pd

import os
import sys
import pandas as pd

sys.path.append(os.getcwd())

from src.data_loader import load_data, clean_data, enrich_data_with_users
from src.weather_service import WeatherService
from src.predictor import EnergyPredictor
from src.visualizer import EnergyVisualizer
from src.reporter import generate_html_report

def main():
    print("=== Iniciando Sistema Inteligente de Predicción de Energía ===")
    
    print("\n[Fase 1] Ingesta de Datos...")
    raw_df = load_data('data/enunciado1_energia.csv')
    if raw_df.empty:
        print("No se pudieron cargar los datos. Abortando.")
        return

    clean_df = clean_data(raw_df)
    
    print("\n[Fase 2] Enriquecimiento con API Meteorológica...")
    start_date = clean_df['Fecha'].min().strftime('%Y-%m-%d')
    end_date = clean_df['Fecha'].max().strftime('%Y-%m-%d')
    
    weather_service = WeatherService()
    weather_data = weather_service.fetch_historical_weather(start_date, end_date)
    
    if not weather_data.empty:
        print(f" Datos meteorológicos obtenidos: {weather_data.shape[0]} registros para {start_date} a {end_date}.")
        final_df = pd.merge(clean_df, weather_data, on='Fecha', how='left')
        
        final_df = final_df.ffill().bfill()
    else:
        print(" AVISO: No se pudieron obtener datos del clima. Usando solo datos del CSV.")
        final_df = clean_df

    print("\n[Fase 3] Aplicando Lógica de Negocio (OOP)...")
    final_df = enrich_data_with_users(final_df)
    
    print("\n[Fase 4] Entrenando Modelo Predictivo...")
    predictor = EnergyPredictor()
    X, y = predictor.prepare_data(final_df)
    X_test, y_test, y_pred = predictor.train(X, y)
    
    from sklearn.metrics import mean_squared_error, r2_score
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n[Fase 5] Generando Reportes Visuales...")
    visualizer = EnergyVisualizer()
    visualizer.plot_consumption_trends(final_df)
    visualizer.plot_user_distribution(final_df)
    visualizer.plot_actual_vs_predicted(y_test, y_pred)
    
    generate_html_report(mse, r2, len(final_df))
    
    print("\n=== Sistema Finalizado Exitosamente ===")
    print("Revise el directorio 'output/' para ver los gráficos y el 'reporte_final.html'.")

if __name__ == "__main__":
    main()
