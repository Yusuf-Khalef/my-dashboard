from flask import Flask, render_template
import requests

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

@app.route('/')
def home():
    github = get_github_data('Yusuf-Khalef')
    repos = get_github_repos('Yusuf-Khalef')
    return render_template('index.html', github=github, repos=repos)

@app.route('/about')
def about():
    return "This is my dashboard project."

if __name__ == '__main__':
    app.run(debug=True)
    
