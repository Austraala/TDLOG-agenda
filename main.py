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
from Back.src.algorithm.crypto import encrypt, compare
from Back.src.entities.user import User
from Back.src.entities.task import Task
from Back.src.entities.schemas import UserSchema

app = f.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///database.db'
CORS(app)

# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:///database.db", echo=True)
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
    print(username_form)
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
            return f.jsonify(f.jsonify({"registered": False}), f.jsonify(existent_user))

    # persist user
    session.add(user)
    session.commit()

    # return created user
    new_user = UserSchema().dump(user)
    session.close()
    return f.jsonify(f.jsonify({"registered": False}), f.jsonify(new_user)), 201


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    Session.remove()
