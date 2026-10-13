from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from github_api import get_github_data, get_github_repos, get_language_stats
from weather_api import get_weather
import secrets
from urllib.parse import urlencode
import os 
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

def exchange_code(code):
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
            "code": code,
            "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
        },
        timeout=5,
    )

    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    return None

def get_github_username(token):
    response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get("login")

    return None

#ROUTES
@app.route('/')
def home():
    token = session.get("access_token")
    if not token:
        return render_template('landing.html')
    username = get_github_username(token)
    if not username:
        session.clear()
        return render_template('landing.html')
    
    github = get_github_data(username)
    repos = get_github_repos(username)
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
    return redirect("https://github.com/login/oauth/authorize?" + urlencode(params))

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return "Authentication was denied."
    returned_state = request.args.get("state")
    saved_state = session.pop("oauth_state", None)
    if returned_state != saved_state:
        return "State mismatch.", 400
    
    code = request.args.get("code")
    token = exchange_code(code)
    if token:
        session["access_token"] = token
        return redirect("/")
    return "Failed to obtain access token.", 400
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
    
