from flask import Flask
from flask_cors import CORS
from scripts.snscraper import get_tweet

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def home():
    return 'Hello 310.ai v5'


@app.route('/accounts')
def accounts():
    return [
        {"id": "elonmusk", "name": "Elon Musk", "avatar": "/elonmusk.jpg", "background": "/elonmusk-bg.jpeg"},
        {"id": "barackobama", "name": "Barack Obama", "avatar": "/barackobama.jpg", "background": "/barackobama-bg.jpeg"},
        {"id": "yannlecun", "name": "Yann Lecun", "avatar": "/yannlecun.jpg", "background": "/yannlecun-bg.jpeg"}
    ]


@app.route('/audience')
def audience():
    return 'audience'


@app.route('/sentiment')
def sentiment():
    return 'sentiment'


@app.route('/tweets/<username>')
def tweets(username):
    since = '2023-02-01'
    tweet_list = get_tweet(username=username, since=since)
    return tweet_list
