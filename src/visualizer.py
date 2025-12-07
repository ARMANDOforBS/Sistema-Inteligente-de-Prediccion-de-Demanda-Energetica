import matplotlib.pyplot as plt
import seaborn as sns
import os

class EnergyVisualizer:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def plot_actual_vs_predicted(self, y_test, y_pred):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=y_test, y=y_pred, color='blue', alpha=0.6)
        
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--')
        
        plt.title('Consumo Energético: Real vs Predicho', fontsize=16)
        plt.xlabel('Consumo Real (kWh)', fontsize=12)
        plt.ylabel('Consumo Predicho (kWh)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        save_path = os.path.join(self.output_dir, 'prediccion_vs_real.png')
        plt.savefig(save_path)
        plt.close()
        print(f"Gráfico guardado en: {save_path}")

    def plot_consumption_trends(self, df):
        plt.figure(figsize=(12, 6))
        
        if 'Fecha' in df.columns and 'Consumo_kWh' in df.columns:
            sns.lineplot(data=df, x='Fecha', y='Consumo_kWh', hue='Usuario', marker='o')
            plt.title('Tendencia de Consumo Energético por Fecha y Tipo', fontsize=16)
            plt.xlabel('Fecha', fontsize=12)
            plt.ylabel('Consumo (kWh)', fontsize=12)
            plt.grid(True)
            
            save_path = os.path.join(self.output_dir, 'tendencia_consumo.png')
            plt.savefig(save_path)
            plt.close()
            print(f"Gráfico guardado en: {save_path}")

    def plot_user_distribution(self, df):
        plt.figure(figsize=(8, 6))
        if 'Usuario' in df.columns:
            sns.barplot(data=df, x='Usuario', y='Consumo_kWh', estimator='mean', errorbar=None, palette='viridis')
            plt.title('Consumo Promedio por Tipo de Usuario', fontsize=16)
            plt.ylabel('Consumo Promedio (kWh)')
            
            save_path = os.path.join(self.output_dir, 'distribucion_usuarios.png')
            plt.savefig(save_path)
            plt.close()
            print(f"Gráfico guardado en: {save_path}")
