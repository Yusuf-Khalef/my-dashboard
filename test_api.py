from collections import Counter
import os 
from dotenv import load_dotenv
import requests

github_response = requests.get("https://api.github.com/users/Yusuf-Khalef/repos")
data = github_response.json()

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
print(api_key is not None)

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": "brampton",
    "appid": api_key,
    "units": "metric",
}
weather_response = requests.get(url, params=params, timeout=5)
weather_data = weather_response.json()
print(weather_response.status_code)
print(weather_data)

temperature = weather_data["main"]["temp"] if "main" in weather_data and "temp" in weather_data["main"] else None
feels_like = weather_data["main"]["feels_like"] if "main" in weather_data and "feels_like" in weather_data["main"] else None
description = weather_data["weather"][0]["description"] if "weather" in weather_data and len(weather_data["weather"]) > 0 else None
print(f"The temperature in Brampton is {temperature}°C.")
print(f"It feels like {feels_like}°C.")
print(f"Weather description: {description}.")


'''
languages = [repo.get("language") for repo in data if repo.get("language") is not None]
print(languages)
counter_languages = Counter(languages)
print(counter_languages.most_common(1))
print(counter_languages.most_common())'''


'''if response.status_code == 200:
    data = response.json()
    print("Followers:", data["followers"])
elif response.status_code == 404:
    print("That user doesn't exist.")
else:
    print("Something went wrong. Status code:", response.status_code)'''