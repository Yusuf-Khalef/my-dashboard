from flask import Flask, render_template, request
from dotenv import load_dotenv
from github_api import get_github_data, get_github_repos, get_language_stats
from weather_api import get_weather

load_dotenv()

app = Flask(__name__)

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
    
