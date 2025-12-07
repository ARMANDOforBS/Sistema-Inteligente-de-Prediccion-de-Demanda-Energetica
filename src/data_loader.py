import pandas as pd
import numpy as np

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print(f"Datos cargados exitosamente: {df.shape[0]} registros.")
        return df
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {filepath}")
        return pd.DataFrame()

def clean_data(df):
    df_clean = df.dropna().copy()
    
    if 'Fecha' in df_clean.columns:
        df_clean['Fecha'] = pd.to_datetime(df_clean['Fecha'])
    
    if 'Consumo_kWh' in df_clean.columns:
         df_clean['Consumo_kWh'] = pd.to_numeric(df_clean['Consumo_kWh'], errors='coerce')

    return df_clean

def normalize_features(df, feature_cols):
    df_norm = df.copy()
    for col in feature_cols:
        if col in df_norm.columns:
            col_data = df_norm[col].values
            min_val = np.min(col_data)
            max_val = np.max(col_data)
            if max_val - min_val != 0:
                df_norm[col] = (col_data - min_val) / (max_val - min_val)
    return df_norm

def enrich_data_with_users(df):
    from src.models import factory_usuario
    
    if 'Usuario' not in df.columns:
        return df
    
    user_objects = df['Usuario'].apply(factory_usuario)
    
    df['Tarifa_Base'] = user_objects.apply(lambda u: u.calcular_tarifa_base())
    
    return df
