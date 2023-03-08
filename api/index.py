from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def home():
    return 'Hello 310.ai'

@app.route('/accounts')
def accounts():
    return [{ "name": "Elon Musk", "avatar": "", "background": "" }]

@app.route('/audience')
def audience():
    return 'audience'

@app.route('/sentiment')
def sentiment():
    return 'sentiment'
    
@app.route('/tweets')
def tweets():
    return 'tweets'