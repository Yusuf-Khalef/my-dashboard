from flask import Flask, render_template, request
import requests
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_github_data(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
    except requests.exceptions.RequestException:
        return None
    if response.status_code == 200:
        return response.json()
    return None
    
def get_github_repos(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}/repos", timeout=5)
    except requests.exceptions.RequestException:
        return None
    if response.status_code == 200:
        return response.json()
    return None

def get_language_stats(repos):
    if not repos:
        return []
    languages = [repo.get("language") for repo in repos if repo.get("language") is not None]
    counter_languages = Counter(languages)
    return counter_languages.most_common()

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

#ROUTES
@app.route('/')
def home():
    github = get_github_data('Yusuf-Khalef')
    repos = get_github_repos('Yusuf-Khalef')
    count = get_language_stats(repos)
    city = request.args.get('city', 'brampton')
    weather = get_weather(city)  
    return render_template('index.html', github=github, repos=repos, count=count, weather=weather)

@app.route('/about')
def about():
    return "This is my dashboard project."

if __name__ == '__main__':
    app.run(debug=True)
    
