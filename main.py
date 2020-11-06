"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""

import flask as f
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import crypto
from task import User

# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:////database.db", echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
app = f.Flask(__name__)
app.debug = True

logged_in_list = []


@app.route('/')
def log():
    """ Displays a welcome page with log in / sign in possibilities """

    if logged_in_list:
        username = logged_in_list[-1]
        session = Session()
        user = session.query(User).filter(User.username == username).first()
        session.close()
        return f.render_template("home.html", user=user)
    return "You are not logged in <br><a href = '/login'></b>click here to log in</b>" \
           "</a><a href = '/register'></b>click here to sign in</b></a>"


@app.route('/register', methods=['POST', 'GET'])
def register():
    """ Allows user to sign in """

    if f.request.method == 'POST':
        user_to_add = User(f.request.form['username'], crypto.encrypt(f.request.form['password']),
                           f.request.form['gender'], f.request.form['email'])
        session = Session()
        user_list = session.query(User).all()
        for user in user_list:
            print(user, user_to_add)
            if user == user_to_add:
                existent_username = user.username
                session.commit()
                session.close()
                return f.render_template("register.html", existent_username=existent_username)
            else:
                session.add(user_to_add)
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
        user_candidate_list = session.query(User).filter(User.username == username_form)
        for user in user_candidate_list:
            if crypto.compare(password_form, user.password):
                logged_in_list.append(username_form)
                session.close()
                return f.redirect(f.url_for('log'))
    return f.render_template("login.html")


@app.route('/logout/<username>')
def logout(username):
    """ Remove the username from the session if it is there """
    print(logged_in_list, '{}'.format(username))
    logged_in_list.remove('{}'.format(username))
    return f.redirect(f.url_for('log'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    Session.remove()
