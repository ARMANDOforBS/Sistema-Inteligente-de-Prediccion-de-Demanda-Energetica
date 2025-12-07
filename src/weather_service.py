import requests
import pandas as pd

class WeatherService:
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    def __init__(self, lat=-12.0464, lon=-77.0428):
        # Lima, Perú
        self.lat = lat
        self.lon = lon

    def fetch_historical_weather(self, start_date, end_date):
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": "auto"
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'daily' in data:
                daily_data = data['daily']
                df_weather = pd.DataFrame({
                    'Fecha': pd.to_datetime(daily_data['time']),
                    'Temp_Max_API': daily_data['temperature_2m_max'],
                    'Temp_Min_API': daily_data['temperature_2m_min'],
                    'Precip_API': daily_data['precipitation_sum']
                })
                df_weather['Temp_Promedio_API'] = (df_weather['Temp_Max_API'] + df_weather['Temp_Min_API']) / 2
                return df_weather
            else:
                print("No 'daily' data found in API response.")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return pd.DataFrame()
