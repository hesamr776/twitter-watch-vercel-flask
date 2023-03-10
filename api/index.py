from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

since = '2023-02-01'

@app.route('/')
def home():
    return 'Hello 310.ai v8'


@app.route('/accounts')
def accounts():
    return [
        {"id": "elonmusk", "name": "Elon Musk", "avatar": "/elonmusk.jpg", "background": "/elonmusk-bg.jpeg"},
        {"id": "barackobama", "name": "Barack Obama", "avatar": "/barackobama.jpg", "background": "/barackobama-bg.jpeg"},
        {"id": "yannlecun", "name": "Yann Lecun", "avatar": "/yannlecun.jpg", "background": "/yannlecun-bg.jpeg"}
    ]


@app.route('/audience/<username>')
def audience(username):
    return [
        { "id": "elonmusk", "avatar": "/elonmusk.jpg" },
        { "id": "barackobama", "avatar": "/barackobama.jpg" },
        { "id": "yannlecun", "avatar": "/yannlecun.jpg" }
    ]


@app.route('/sentiment')
def sentiment():
    return 'sentiment'


@app.route('/tweets/<username>')
def tweets(username):
    return [
        {
            "username": username,
            "id": "1234567",
            "avatar": "/elonmusk.jpg",
            "date": "10h",
            "text": 'just human rights',
            "sentiment": 1
        },
        {
            "username": username,
            "id": "8765432",
            "avatar": "/elonmusk.jpg",
            "date": "1d",
            "text": 'you are bad',
            "sentiment": 0
        },
        {
            "username": username,
            "id": "12345678",
            "avatar": "/elonmusk.jpg",
            "date": "2d",
            "text": 'normal tweet message',
            "sentiment": 1
        }
    ]
   
