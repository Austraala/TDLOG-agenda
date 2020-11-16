"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""

import flask as f
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from Back.src.algorithm.crypto import encrypt, compare
from Back.src.entities.user import User
from Back.src.entities.task import Task
from Back.src.entities.schemas import UserSchema

app = f.Flask(__name__, static_folder="Front/src/Static", template_folder="Front/src/Templates")
CORS(app)

# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:////database.db", echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

logged_in_list = []


@app.route('/')
def log():
    """ Displays a welcome page with log in / sign in possibilities """

    if logged_in_list:
        username = logged_in_list[-1]
        session = Session()
        user = session.query(User).filter(User.username == username).first()
        task_list = session.query(Task).filter(Task.user_id == User.id).all()
        session.close()
        return f.render_template("navbar.html") +\
               f.render_template("home.html", user=user, tasks=task_list)
    return "You are not logged in <br><a href = '/login'></b>click here to log in</b>" \
           "</a><a href = '/register'></b>click here to sign in</b></a>"


@app.route('/register', methods=['POST', 'GET'])
def register():
    """ Allows user to sign in """

    if f.request.method == 'POST':
        user_to_add = User(f.request.form['username'], encrypt(f.request.form['password']),
                           f.request.form['gender'], f.request.form['email'])
        session = Session()
        user_list = session.query(User).all()
        for user in user_list:
            if user == user_to_add:
                existent_username = user.username
                session.commit()
                session.close()
                return f.render_template("register.html",
                                         existent_username="Username "
                                                           + str(existent_username)
                                                           + " already taken")
            # else:
            #    session.add(user_to_add)
            #    session.commit()
            #    session.close()
            #    return f.redirect(f.url_for('log'))
    return f.render_template("register.html", existent_username="")


@app.route('/login_back', methods=['POST', 'GET'])
def login():
    """ If the connection information fits database, adds user to logged in list"""

    if f.request.method == 'POST':
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


@app.route('/logout_back', methods=['POST', 'GET'])
def logout():
    """ Remove the username from the session if it is there """
    if f.request.method == 'POST':
        user_form = f.request.json
        username_form = user_form['username']
        empty_user = User("", "", "", "")
        new_empty_user = UserSchema().dump(empty_user)
        print("---------------------", logged_in_list)
        logged_in_list.remove('{}'.format(username_form))
        print("---------------------", logged_in_list)
        return f.jsonify(new_empty_user)
    return 0


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


@app.route('/users', methods=['POST'])
def add_user():
    """ Adds an user to the database """
    # mount user object
    posted_user = UserSchema(only='username')\
        .load(f.request.get_json())

    user = User(**posted_user.data, created_by="HTTP post request")

    # persist user
    session = Session()
    session.add(user)
    session.commit()

    # return created user
    new_user = UserSchema().dump(user).data
    session.close()
    return f.jsonify(new_user), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    Session.remove()
