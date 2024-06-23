from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request , json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
from UserM import UserM
from TaskM import TaskM
from flask.cli import with_appcontext, click
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'
engine = create_engine('sqlite:///your_database_name.db')
Base = declarative_base()
#Initialize The Database
db = SQLAlchemy(app)
"""
@app.cli.command('create-db')
@with_appcontext
def create_db():
    db.create_all()
    click.echo('Database and tables created.')
"""



# Create Model For Users
class User(Base):
    #This line specifies the name of the database table
    __tablename__ = 'User'
    #This line creates a column named id, whose type is integer and is known as primary_key.
    id = Column(Integer,  primary_key=True)
    user_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    user_pass = Column(String(200), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

    tasks = relationship('Task', backref='assigneddd_user', lazy=True)



# Create Model For Tasks
class Task(Base):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True)
    task_title = Column(String(100))
    task_dsc = Column(String(1000))
    task_done = Column(Boolean, default=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    assigned_user = relationship("User", backref="taskss", lazy='select')



def __init__():
    return app

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Edit task done
@app.route('/task/<int:task_id>/status', methods=['POST'])
#The task_id is passed as an argument to this function and its value is taken from the URL.
def update_task_status(task_id):
    task = session.query(Task).get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task.task_done = data.get('task_done', task.task_done)

    session.commit()
    return jsonify({'message': 'Task status updated successfully'})

# Edit password
@app.route('/user/<int:user_id>/password', methods=['POST'])
def edit_user_password(user_id):

    # get user by user_id
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        data = request.json
        # changes user_pass to new user pass
        user.user_pass = data.get('user_pass', user.user_pass)

        # add all changes
        session.commit()
        return jsonify({'message': 'Password updated successfully'})
    else:
        return jsonify({'message': 'User not found'})



# Edit Task
@app.route('/tasks/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task = session.query(Task).get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    data = request.get_json()
    task.task_title = data.get('task_title')
    task.task_dsc = data.get('task_dsc')
    task.task_done = data.get('task_done')
    
    session.commit()
    
    return jsonify({'message': 'Task updated successfully'})

# Remove the task.
@app.route('/task/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'message': 'Task not found'})


# get users tasks
@app.route('/user/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    tasks = session.query(Task).filter_by(user_id=user_id).all()
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



def getJsonData():

    myJsonData = {}

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        myJsonData = request.json
    else:
        data = json.loads(request.data)
        myJsonData = data

    return myJsonData



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # check if user name and password are exist in database if it exists returm taht user
    user = session.query(User).filter_by(user_name = username, user_pass = password).first()
    if user is not None:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'}, 401)
    


@app.route("/signup", methods=['POST'])
def user_signup():
    myJsonData = request.get_json()

    

    # Add User To The Database
    user = session.query(User).filter_by(email=myJsonData.get("user_email")).first()
    if user is None:
        user = User(
            user_name = myJsonData.get("user_name"),
            email = myJsonData.get("user_email"),
            user_pass = myJsonData.get("user_pass")  
            )
        session.add(user)
        session.commit()
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
    my_task = TaskM()

    try:
        my_task.task_title = jsonData.get("task_title")
        my_task.task_dsc = jsonData.get("task_dsc")
        my_task.task_done = jsonData.get("task_done")
        return my_task
    except:
        return "Error"
    


@app.route("/addTask", methods = ['POST'])
def addTask():
    myJsonData = request.get_json()

    my_task = addTaskDataToModel(myJsonData)

    if my_task == "Error":
        return jsonify({"message": "Error"})
    
    user = session.query(User).filter_by(id=myJsonData.get("user_id")).first()

    if user:
        new_task = Task(task_title=my_task.task_title, task_dsc=my_task.task_dsc, task_done=my_task.task_done)

        user.tasks.append(new_task)
        session.add(new_task)
        session.commit()
        return jsonify({"message" : "added"})
    else:
        return jsonify({"message": "User not found"})
    

