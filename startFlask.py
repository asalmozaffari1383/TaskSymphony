from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request , json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from User import User

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'

#Initialize The Database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    user_pass = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.user_name



def __init__():
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


@app.route("/login", methods=['POST'])
def user_login():
    
    myJsonData = {}

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        myJsonData = request.json
    else:
        data = json.loads(request.data)
        myJsonData = data

    my_user = User()
    try:
        my_user.user_name = myJsonData.get("user_name")
        my_user.user_email = myJsonData.get("user_email")
        my_user.user_pass = myJsonData.get("user_pass")
        return my_user
    except:
        return myJsonData


@app.route("/signup", methods=['POST'])
def user_signup():
    myJsonData = {}

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        myJsonData = request.json
    else:
        data = json.loads(request.data)
        myJsonData = data

    my_user = User()
    try:
        my_user.user_name = myJsonData.get("user_name")
        my_user.user_email = myJsonData.get("user_email")
        my_user.user_pass = myJsonData.get("user_pass")

    except:
        return myJsonData
    

    # Add User To The Database
    if my_user is not None:
        user = Users.query.filter_by(email=my_user.user_email).first()
        if user is None:
            user = Users(
                user_name = my_user.user_name,
                email = my_user.user_email,
                user_pass = my_user.user_pass
                )
            db.session.add(user)
            db.session.commit()
            return "OK"
        else:
            return "Already Exist"


@app.route("/getAllUsers")
def getAllUsers():
    our_users = Users.query.order_by(Users.date_added)

    t = ""
    for i in our_users:
        t += i.email + " "

    return t


    #return str(type(our_users))
