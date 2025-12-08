import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
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
            
    def plot_consumption_trend_interactive(self, df):
        plot_bg_color = 'rgba(0,0,0,0)'
        text_color = '#e6edf3'
        
        # Prepare custom data for hover (handle missing weather cols if necessary)
        extra_cols = []
        hover_template_extra = ""
        
        if 'Temp_Promedio_API' in df.columns and 'Precip_API' in df.columns:
            extra_cols = ['Temp_Promedio_API', 'Precip_API']
            hover_template_extra = "<br><b>Temp:</b> %{customdata[0]:.1f} °C<br><b>Lluvia:</b> %{customdata[1]:.1f} mm"

        fig_trend = px.line(df, x='Fecha', y='Consumo_kWh', color='Usuario',
                            color_discrete_sequence=px.colors.qualitative.Pastel,
                            custom_data=extra_cols if extra_cols else None)
        
        fig_trend.update_traces(
            mode="lines",
            hovertemplate=f"<b>Fecha:</b> %{{x|%Y-%m-%d}}<br><b>Consumo:</b> %{{y:.2f}} kWh{hover_template_extra}<extra></extra>"
        )
        fig_trend.update_layout(
            plot_bgcolor=plot_bg_color,
            paper_bgcolor=plot_bg_color,
            font_color=text_color,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#30363d'),
            hoverlabel=dict(
                bgcolor="#0d1117",
                font_size=14,
                font_family="sans-serif",
                bordercolor="#30363d"
            )
        )
        return fig_trend

    def plot_user_distribution_interactive(self, df):
        plot_bg_color = 'rgba(0,0,0,0)'
        text_color = '#e6edf3'
        
        fig_bar = px.bar(df.groupby('Usuario')['Consumo_kWh'].mean().reset_index(), 
                         x='Usuario', y='Consumo_kWh', color='Usuario',
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig_bar.update_traces(
            hovertemplate="<b>Usuario:</b> %{x}<br><b>Promedio:</b> %{y:.2f} kWh<extra></extra>"
        )
        fig_bar.update_layout(
            plot_bgcolor=plot_bg_color,
            paper_bgcolor=plot_bg_color,
            font_color=text_color,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            hoverlabel=dict(
                bgcolor="#0d1117",
                font_size=14,
                font_family="sans-serif",
                bordercolor="#30363d"
            )
        )
        return fig_bar
        
    def plot_prediction_validation_interactive(self, df_pred):
        plot_bg_color = 'rgba(0,0,0,0)'
        text_color = '#e6edf3'
        
        # Calculate errors for tooltip context
        df_pred = df_pred.copy()
        df_pred['Error_kWh'] = df_pred['Predicho'] - df_pred['Real']
        df_pred['Error_Abs'] = df_pred['Error_kWh'].abs()
        
        fig_scatter = px.scatter(df_pred, x='Real', y='Predicho', opacity=0.7,
                                 color_discrete_sequence=['#58a6ff'],
                                 custom_data=['Error_kWh', 'Error_Abs'])
                                 
        fig_scatter.add_trace(go.Scatter(x=[df_pred['Real'].min(), df_pred['Real'].max()], 
                                         y=[df_pred['Real'].min(), df_pred['Real'].max()],
                                         mode='lines', name='Ideal', line=dict(color='#fd8c73', dash='dash'),
                                         hoverinfo='skip')) # Skip hover for the line
        
        fig_scatter.update_traces(
            hovertemplate="<b>Real:</b> %{x:.0f} kWh<br><b>Pred:</b> %{y:.0f} kWh<br><b>Diff:</b> %{customdata[0]:+.0f} kWh<extra></extra>",
            selector=dict(type='scatter', mode='markers')
        )

        fig_scatter.update_layout(
            plot_bgcolor=plot_bg_color,
            paper_bgcolor=plot_bg_color,
            font_color=text_color,
            xaxis=dict(showgrid=True, gridcolor='#30363d'),
            yaxis=dict(showgrid=True, gridcolor='#30363d'),
            hoverlabel=dict(
                bgcolor="#0d1117",
                font_size=14,
                font_family="sans-serif",
                bordercolor="#30363d"
            )
        )
        return fig_scatter
