"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""

import flask as f
import command_db as db
import crypto

app = f.Flask(__name__)
app.debug = True

Session = {}


@app.route('/')
def log():
    if 'username' in Session:
        username = Session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>click here to log in</b>" \
           "</a><a href = '/register'></b>click here to sign in</b></a>"


@app.route('/register', methods=['POST', 'GET'])
def register():
    if f.request.method == 'POST':
        db.add_user(f.request.form['username'], crypto.encrypt(f.request.form['password']),
                    f.request.form['gender'], f.request.form['email'])
        return f.redirect(f.url_for('log'))
    return f.render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    """ If the connection information fits database, create a session"""
    if f.request.method == 'POST':
        username_try = f.request.form['username']
        password_try = f.request.form['password'].encode('utf-8')
        request = '''SELECT * FROM users WHERE username = "{0}"'''.format(username_try)
        for user in db.use_db(request):
            if crypto.compare(password_try, user[2]):
                Session['username'] = username_try
                return f.redirect(f.url_for('log'))
    return f.render_template("login.html")


@app.route('/logout')
def logout():
    """ Remove the username from the session if it is there """
    Session.pop('username', None)
    return f.redirect(f.url_for('log'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
