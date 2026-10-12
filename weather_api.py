import requests
import os

from cache import get_cache 

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    cached = get_cache(f"weather: {city.lower()}")
    if cached is not None:
        return cached
    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException:
        return None
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
        }
    return None