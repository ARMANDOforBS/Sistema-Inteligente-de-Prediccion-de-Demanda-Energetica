from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np

class EnergyPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.feature_cols = []

    def prepare_data(self, df):
        if 'Usuario' in df.columns:
            df = pd.get_dummies(df, columns=['Usuario'], prefix='UserType', drop_first=True)
        
        potential_features = [
            'Temperatura_C', 'Humedad_%', 'Tarifa_Base', 
            'Temp_Promedio_API', 'Precip_API'
        ]
        
        dummy_cols = [col for col in df.columns if col.startswith('UserType_')]
        potential_features.extend(dummy_cols)
        
        self.feature_cols = [col for col in potential_features if col in df.columns]
        
        df_ml = df.dropna(subset=self.feature_cols + ['Consumo_kWh'])
        
        X = df_ml[self.feature_cols]
        y = df_ml['Consumo_kWh']
        
        return X, y

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("\n--- Resultados del Entrenamiento ---")
        print(f"Features usadas: {self.feature_cols}")
        print(f"MSE: {mse:.2f}")
        print(f"R2 Score: {r2:.4f}")
        
        return X_test, y_test, y_pred

    def predict_future(self, input_data):
        return self.model.predict(input_data)
