from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request , json




app = Flask(__name__)

def __init__():
    from . import db
    db.init_app(app)

    return app
"""

@app.route("/")
def hello():
    return "<p>Hello Mother Fucker!!</p>"

@app.route("/login")
def login():
    return "login"

@app.route("/user/<username>")
def profile(username):
    return f'{username}\'s profile'
@app.route("/data")
def get_data():
    return {
        "name" : "mahdi",
        "xx" : [1,2,3]
    }
"""
@app.route("/data", methods=['POST', 'GET'])
def get_data():
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            return request.json
        else:
            data = json.loads(request.data)
            return data
        # TODO: make Post method

    elif request.method == "GET":
        # TODO: make Get method
        pass


