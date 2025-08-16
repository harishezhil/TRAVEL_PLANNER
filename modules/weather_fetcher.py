import os
import requests
from datetime import datetime, timedelta

class WeatherFetcher:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_weather_forecast(self, destination, start_date, end_date):
        if not self.api_key:
            raise ValueError("Missing OPENWEATHER_API_KEY in environment variables.")

        # Call OpenWeatherMap API
        params = {
            "q": destination,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Weather API failed: {response.text}")

        forecast_data = response.json()
        weather_list = []

        # Parse only the dates we need
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        for entry in forecast_data["list"]:
            date_txt = entry["dt_txt"].split(" ")[0]
            date_obj = datetime.strptime(date_txt, "%Y-%m-%d")
            if start_dt <= date_obj <= end_dt:
                weather_list.append({
                    "date": date_txt,
                    "temp": entry["main"]["temp"],
                    "weather": entry["weather"][0]["description"]
                })

        return weather_list
