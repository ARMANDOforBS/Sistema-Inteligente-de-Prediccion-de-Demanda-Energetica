import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data():
    total_records = 3000
    users = ['Residencial', 'Comercial', 'Industrial']
    records_per_day = len(users)
    days_needed = total_records // records_per_day
    
    end_date = datetime(2025, 12, 5) 
    start_date = end_date - timedelta(days=days_needed - 1)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    
    print(f"Generando datos REALISTAS (con caos) desde {start_date.date()} hasta {end_date.date()}")
    
    for single_date in date_range:
        date_str = single_date.strftime('%Y-%m-%d')
        day_of_year = single_date.timetuple().tm_yday
        weekday = single_date.weekday() # 0=Lunes, 6=Domingo
        
        # Temperatura con ruido
        base_temp = 15 + 15 * np.sin(2 * np.pi * (day_of_year - 60) / 365)
        temp_c = int(base_temp + random.uniform(-8, 8)) # Más varianza diaria
        
        humidity = int(random.uniform(20, 95))
        
        # Eventos aleatorios globales (ej. Ola de calor, falla eléctrica)
        global_multiplier = 1.0
        if random.random() < 0.02: # 2% probabilidad de evento extremo
            type_event = random.choice(['OlaCalor', 'FallaRed'])
            if type_event == 'OlaCalor':
                global_multiplier = 1.4 # Consumo se dispara
            else:
                global_multiplier = 0.6 # Apagón parcial
        
        for user in users:
            base_consumption = 0
            
            # --- Lógica Residencial ---
            if user == 'Residencial':
                # Fines de semana consumen más en residencial
                weekend_factor = 1.2 if weekday >= 5 else 1.0
                base_consumption = (300 + (temp_c * 5)) * weekend_factor
                variation = random.uniform(-0.2, 0.4) # Variación porcentual (-20% a +40%)
                
            # --- Lógica Comercial ---
            elif user == 'Comercial':
                # Fines de semana consumen MENOS en comercial
                workday_factor = 0.5 if weekday >= 5 else 1.2
                base_consumption = (600 + (temp_c * 8)) * workday_factor
                variation = random.uniform(-0.1, 0.3)

            # --- Lógica Industrial ---
            elif user == 'Industrial':
                # Industrial es más constante, pero tiene paradas de mantenimiento
                base_consumption = 1500
                if random.random() < 0.05: # 5% probabilidad de paro por mantenimiento
                    base_consumption = 200 # Solo consumo esencial
                variation = random.uniform(-0.1, 0.1)
            
            # Cálculo final
            consumo = base_consumption * (1 + variation) * global_multiplier
            
            # Ruido puro adicional
            consumo += random.randint(-50, 50)
            
            consumo = int(max(0, consumo))
            
            data.append([date_str, user, consumo, temp_c, humidity])
            
    df = pd.DataFrame(data, columns=['Fecha', 'Usuario', 'Consumo_kWh', 'Temperatura_C', 'Humedad_%'])
    
    if len(df) > 3000:
        df = df.head(3000)
    
    output_path = 'data/enunciado1_energia.csv'
    df.to_csv(output_path, index=False)
    print(f"¡Generado archivo realista {output_path} con {len(df)} registros!")

if __name__ == "__main__":
    generate_data()
