"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""

import flask as f
import crypto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from task import Base, User, Task, FixedTask, MobileTask

# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:////database.db", echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
app = f.Flask(__name__)
app.debug = True

logged_in_list = {}


@app.route('/')
def log():
    """ Displays a welcome page with log in / sign in possibilities """

    if 'username' in logged_in_list:
        username = logged_in_list['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>click here to log in</b>" \
           "</a><a href = '/register'></b>click here to sign in</b></a>"


@app.route('/register', methods=['POST', 'GET'])
def register():
    """ Allows user to sign in """

    if f.request.method == 'POST':
        user = User(f.request.form['username'], crypto.encrypt(f.request.form['password']),
                    f.request.form['gender'], f.request.form['email'])
        session = Session()
        session.add(user)
        session.commit()
        session.close()
        return f.redirect(f.url_for('log'))
    return f.render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    """ If the connection information fits database, create a session"""

    if f.request.method == 'POST':
        username_form = f.request.form['username']
        password_form = f.request.form['password'].encode('utf-8')
        session = Session()
        user_list = session.query(User).filter(User.username == username_form)
        for user in user_list:
            if crypto.compare(password_form, user.password):
                logged_in_list['username'] = username_form
                session.close()
                return f.redirect(f.url_for('log'))
    return f.render_template("login.html")


@app.route('/logout')
def logout():
    """ Remove the username from the session if it is there """

    logged_in_list.pop('username', None)
    return f.redirect(f.url_for('log'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    Session.remove()
