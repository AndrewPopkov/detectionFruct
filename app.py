from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'this is a Flask'

app.run('0.0.0.0:8000', debug=True)