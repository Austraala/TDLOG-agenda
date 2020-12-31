"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""

import flask as f
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import time
from algorithm.crypto import encrypt, compare
from entities.user import User
from entities.task import Task
from entities.schemas import UserSchema, TaskSchema

app = f.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:////database.db'
CORS(app)

# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:////database.db", echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

logged_in_list = []


@app.route('/login_back', methods=['POST'])
def login():
    """ If the connection information fits database, adds user to logged in list"""

    user_form = f.request.json
    username_form = user_form['username']
    password_form = user_form['password'].encode('utf-8')
    session = Session()
    user_candidate_list = session.query(User).filter(User.username == username_form)
    for user in user_candidate_list:
        if compare(password_form, user.password):
            print("---------------------", logged_in_list)
            logged_in_list.append(username_form)
            print("---------------------", logged_in_list)
            session.close()
            return f.jsonify(True)
    return f.jsonify(False)


@app.route('/logout_back', methods=['POST'])
def logout():
    """ Remove the username from the session if it is there """
    user_form = f.request.json
    username_form = user_form['username']
    print("---------------------", logged_in_list)
    logged_in_list.remove('{}'.format(username_form))
    print("---------------------", logged_in_list)
    return f.jsonify(True)


@app.route('/register', methods=['POST'])
def register():
    """ Adds an user to the database """
    # mount user object

    user_form = f.request.json
    user = User(user_form['username'], encrypt(user_form['password']),
                user_form['gender'], user_form['email'])

    # returns false if an user already exists with that username
    session = Session()
    user_list = session.query(User).all()
    for existent_user in user_list:
        if existent_user.username == user.username:
            session.close()
            return f.jsonify(False)

    # persist user
    session.add(user)
    session.commit()

    # return true if it worked
    session.close()
    return f.jsonify(True), 201


@app.route('/users')
def get_users():
    """ Grabs all users in the database """
    # fetching from the database
    session = Session()
    user_objects = session.query(User).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    users = schema.dump(user_objects)

    # serializing as JSON
    session.close()
    return f.jsonify(users)


@app.route('/user', methods=['POST'])
def get_user():
    """ Grabs all users in the database """
    # fetching from the database

    username = f.request.json
    session = Session()
    user = session.query(User).filter(User.username == username['username']).first()

    # transforming into JSON-serializable objects
    schema = UserSchema()
    user = schema.dump(user)

    # serializing as JSON
    session.close()
    return f.jsonify(user)


@app.route('/tasks', methods=['POST'])
def get_tasks():
    """ Grabs all tasks for the selected user in the database """
    # fetching from the database
    user_front = f.request.json

    session = Session()
    task_objects = session.query(Task).filter(Task.user_id == user_front['id']).all()

    # transforming into JSON-serializable objects
    schema = TaskSchema(many=True)
    tasks = schema.dump(task_objects)

    # serializing as JSON
    session.close()
    return f.jsonify(tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    """ Adds a task to the current user """
    # mount task object
    task_form = f.request.json

    session = Session()
    user = session.query(User).filter(User.username == task_form['user']['username']).first()
    task = Task(user.id, task_form['name'], task_form['duration'], task_form['difficulty'])

    # persist task
    session.add(task)
    session.commit()

    # return true
    session.close()
    return f.jsonify(True), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    Session.remove()
