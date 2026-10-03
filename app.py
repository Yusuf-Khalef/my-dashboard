from flask import Flask, render_template
import requests
from collections import Counter

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

@app.route('/')
def home():
    github = get_github_data('Yusuf-Khalef')
    repos = get_github_repos('Yusuf-Khalef')
    count = get_language_stats(repos)
    return render_template('index.html', github=github, repos=repos, count=count)

@app.route('/about')
def about():
    return "This is my dashboard project."

if __name__ == '__main__':
    app.run(debug=True)
    
