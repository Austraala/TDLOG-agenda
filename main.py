"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

import flask as f

app = f.Flask(__name__)
app.debug = True

Session = {}


@app.route('/')
def log():
    if 'username' in Session:
        username = Session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
           "click here to log in</b></a>"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if f.request.method == 'POST':
        Session['username'] = f.request.form['username']
        return f.redirect(f.url_for('log'))
    return f.render_template("login.html")


@app.route('/logout')
def logout():
    """ remove the username from the session if it is there """
    Session.pop('username', None)
    return f.redirect(f.url_for('log'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
