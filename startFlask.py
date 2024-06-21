from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request , json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify

from User import User
from Task import Task

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'

#Initialize The Database
db = SQLAlchemy(app)

# Create Model For Users
class User(db.Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer,  primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    user_pass = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.user_name


# Create Model For Tasks
class Task(db.Base):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(100))
    task_dsc = db.Column(db.String(1000))
    task_done = db.Column(db.Boolean, default=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", backref="tasks")

    def __repr__(self):
        return '<Title %r>' % self.task_title


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

# Edit Task
@app.route('/tasks/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    data = request.get_json()
    task.task_title = data.get('task_title')
    task.task_dsc = data.get('task_dsc')
    task.task_done = data.get('task_done')
    
    db.session.commit()
    
    return jsonify({'message': 'Task updated successfully'})

# Remove the task.
@app.route('/task/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'message': 'Task not found'})


# get users tasks
@app.route('/user/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    tasks = Task.query.filter_by(user_id=user_id).all()
    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'task_title': task.task_title,
            'task_dsc': task.task_dsc,
            'task_done': task.task_done,
            'date_added': task.date_added
        }
        task_list.append(task_data)
    
    return jsonify({'tasks': task_list})

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


def getJsonData():

    myJsonData = {}

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        myJsonData = request.json
    else:
        data = json.loads(request.data)
        myJsonData = data

    return myJsonData


def addUserDataToModel(JsonData):
    my_user = User()
    try:
        my_user.user_name = JsonData.get("user_name")
        my_user.user_email = JsonData.get("user_email")
        my_user.user_pass = JsonData.get("user_pass")
        return my_user
    except:
        return "Error"


@app.route("/login", methods=['POST'])
def user_login():
    
    myJsonData = getJsonData()

    my_user = addUserDataToModel(myJsonData)

    if my_user == "Error":
        return myJsonData
    else:
        return my_user
    


@app.route("/signup", methods=['POST'])
def user_signup():
    myJsonData = getJsonData()

    my_user = addUserDataToModel(myJsonData)

    if my_user == "Error":
        return myJsonData
    

    # Add User To The Database
    if my_user is not None:
        user = User.query.filter_by(email=my_user.user_email).first()
        if user is None:
            user = User(
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
    our_users = User.query.order_by(User.date_added)

    #todo
    t = ""
    for i in our_users:
        t += i.email + " "

    return t


    #return str(type(our_users))


def addTaskDataToModel(jsonData):
    my_task = Task()
    try:
        my_task.task_title = jsonData.get("task_title")
        my_task.task_dsc = jsonData.get("task_dsc")
        my_task.task_done = jsonData.get("task_done")
        return my_task
    except:
        return "Error"
    

@app.route("/addTask", methods = ['POST'])
def addTask():
    myJsonData = getJsonData()

    my_task = addTaskDataToModel(myJsonData)

    if my_task == "Error":
        return myJsonData
    
    """
    if my_task is not None:
        task = None
        task = Task(
            task_title = my_task.task_title,
            task_dsc = my_task.task_dsc,
            task_done = my_task.task_done
        )
        db.session.add(task)
        db.session.commit()
        return "OK"
    else:
        return "Error in adding the Task!"
    
    """    # Add Task TO The Database

    
    # Add Task TO The Database.
    user = db.session.query(User).filter_by(id=myJsonData.get("user_id")).first()

    if user:
        new_task = Task(task_title=my_task.task_title, task_desc=my_task.task_dsc, task_done=my_task.task_done)
        user.tasks.append(new_task)
        db.session.add(new_task)
        db.session.commit()
    else:
        print("User not found")
    
"""
@app.route("/getAllTask")
def getAllTask():
    our_tasks = Task.query.order_by(Task.date_added)

    t = ""
    for i in our_tasks:
        t += i.task_title + " "

        
    return t

"""

