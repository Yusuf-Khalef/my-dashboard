from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from github_api import get_github_data, get_github_repos, get_language_stats
from weather_api import get_weather
import secrets
from urllib.parse import urlencode
import os 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

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

@app.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    params = {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
        "scope": "read:user",
        "state": state,
    }
    return redirect(
    "https://github.com/login/oauth/authorize?" + urlencode(params)
)

if __name__ == '__main__':
    app.run(debug=True)
    
