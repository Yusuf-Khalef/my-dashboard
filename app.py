from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    items = ['Github','Weather', 'Spotify']
    return render_template('index.html', name='Yusuf', items=items)

@app.route('/about')
def about():
    return "This is my dashboard project."

if __name__ == '__main__':
    app.run(debug=True)
    
