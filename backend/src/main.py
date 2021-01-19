"""
This is the main file for dev

   Jean-Loup RAYMOND
   ENPC - (c)

"""
# pylint: disable=E0401

from datetime import datetime
import flask as f
from algorithm.crypto import encrypt, compare
from entities.schemas import UserSchema, FixedTaskSchema, MobileTaskSchema
from entities.task import Task, MobileTask, FixedTask
from entities.user import User
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.anki.anki import create_deck, delete_deck, clear_deck, \
    basic_note, basic_reversed_note, basic_optional_reversed_note, basic_typein_note, cloze_note
from backend.src.algorithm.organize_schedule import organize_schedule

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
            logged_in_list.append(username_form)
            print("---------------------", logged_in_list)
            session.close()
            return f.jsonify(True), 201
    return f.jsonify(False)


@app.route('/logout_back', methods=['POST'])
def logout():
    """ Remove the username from the session if it is there """
    user_form = f.request.json
    username_form = user_form['username']
    logged_in_list.remove('{}'.format(username_form))
    print("---------------------", logged_in_list)
    return f.jsonify(True), 201


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
    return f.jsonify(users), 201


@app.route('/user', methods=['POST'])
def get_user():
    """ Grabs an user in the database from a form """
    # fetching from the database

    username = f.request.json
    session = Session()
    user = session.query(User).filter(User.username == username['username']).first()

    # transforming into JSON-serializable objects
    schema = UserSchema()
    user = schema.dump(user)

    # serializing as JSON
    session.close()
    return f.jsonify(user), 201


@app.route('/mobile_tasks', methods=['POST'])
def get_mobile_tasks():
    """ Grabs all mobile tasks for the selected user in the database """
    # fetching from the database
    user_front = f.request.json
    session = Session()
    mobile_task_objects = \
        session.query(MobileTask).filter(MobileTask.user_id == user_front['id']).all()

    # transforming into JSON-serializable objects
    schema = MobileTaskSchema(many=True)
    mobile_tasks = schema.dump(mobile_task_objects)

    # serializing as JSON
    session.close()
    return f.jsonify(mobile_tasks), 201


@app.route('/add_mobile_task', methods=['POST'])
def add_mobile_task():
    """ Adds a mobile task to the current user """
    # mount task object
    mobile_task_form = f.request.json

    session = Session()
    user = \
        session.query(User).filter(User.username ==
                                   mobile_task_form['task']['user']['username']).first()
    task = Task(user.id, mobile_task_form['task']['name'], mobile_task_form['task']['duration'],
                mobile_task_form['task']['difficulty'])
    mobile_task = MobileTask(task, datetime.strptime(mobile_task_form['deadline'], "%Y-%m-%d"))

    # persist task
    session.add(task)
    session.add(mobile_task)
    session.commit()

    # return true
    session.close()
    return f.jsonify(True), 201


@app.route('/remove_mobile_task', methods=['POST'])
def remove_mobile_task():
    """ Removes a mobile task to the current user
    /// NotImplementedError - change SQLite to PostgreSQL """
    # mount task object
    mobile_task_form = f.request.json

    session = Session()
    user = \
        session.query(User).filter(User.username ==
                                   mobile_task_form['task']['user']['username']).first()
    task = Task(user.id, mobile_task_form['task']['name'], mobile_task_form['task']['duration'],
                mobile_task_form['task']['difficulty'])
    mobile_task = MobileTask(task, datetime.strptime(mobile_task_form['deadline'], "%Y-%m-%d"))

    # remove persisted task
    session.query(Task).filter(Task == task).delete()
    session.query(MobileTask).filter(MobileTask == mobile_task).delete()
    session.commit()

    # return true
    session.close()
    return f.jsonify(True), 201


@app.route('/fixed_tasks', methods=['POST'])
def get_fixed_tasks():
    """ Grabs all fixed tasks for the selected user in the database """
    # fetching from the database
    user_front = f.request.json
    session = Session()
    fixed_task_objects = \
        session.query(FixedTask).filter(FixedTask.user_id == user_front['id']).all()

    # transforming into JSON-serializable objects
    schema = FixedTaskSchema(many=True)
    fixed_tasks = schema.dump(fixed_task_objects)

    # serializing as JSON
    session.close()
    return f.jsonify(fixed_tasks), 201


@app.route('/organize_schedule', methods=['POST'])
def fix_mobile_tasks():
    """ Allocates a fixed period to a mobile task """
    # fetching from the database
    user_front, today = f.request.json[0], f.request.json[1]
    month = int(today[5:7])
    day = int(today[8:10])

    session = Session()
    fixed_task_objects = \
        session.query(FixedTask).filter(FixedTask.user_id == user_front['id']).all()
    mobile_task_objects = \
        session.query(MobileTask).filter(MobileTask.user_id == user_front['id']).all()
    session.close()

    # transforming into JSON-serializable objects
    fixed_task_schema = FixedTaskSchema(many=True)
    fixed_tasks = fixed_task_schema.dump(fixed_task_objects)
    mobile_task_schema = MobileTaskSchema(many=True)
    mobile_tasks = mobile_task_schema.dump(mobile_task_objects)
    list_tasks = list(fixed_tasks) + list(mobile_tasks)

    organize_schedule(list_tasks, month, day)
    return f.jsonify(True), 201


@app.route('/create', methods=['POST'])
def create_anki_deck():
    """ Creates an Anki deck """
    deck_name = f.request
    create_deck(deck_name['name'])
    # We should store it in db
    return f.jsonify(deck_name), 201


@app.route('/delete', methods=['POST'])
def delete_anki_deck():
    """ Deletes an Anki deck """
    deck_name = f.request.json
    delete_deck(deck_name['name'])
    return f.jsonify(deck_name), 201


@app.route('/clear', methods=['POST'])
def clear_anki_deck():
    """ Removes all cards from an Anki deck """
    deck_name = f.request.json
    clear_deck(deck_name['name'])
    return f.jsonify(deck_name), 201


@app.route('/basic', methods=['POST'])
def create_basic_card():
    """ Creates a "Basic"-modelled Anki card """
    basic_note_form = f.request.json
    basic_note(basic_note_form['deck_name'], basic_note_form['front'], basic_note_form['back'])
    return f.jsonify(True), 201


@app.route('/basic_reversed', methods=['POST'])
def create_basic_reversed_card():
    """ Creates a "Basic (and reversed card)"-modelled Anki card """
    basic_reversed_note_form = f.request.json
    basic_reversed_note(basic_reversed_note_form['deck_name'],
                        basic_reversed_note_form['front'],
                        basic_reversed_note_form['back'])
    return f.jsonify(True), 201


@app.route('/basic_optional_reversed', methods=['POST'])
def create_basic_optional_reversed_card():
    """ Creates a "Basic (optional reversed card)"-modelled Anki card """
    basic_optional_reversed_note_form = f.request.json
    basic_optional_reversed_note(basic_optional_reversed_note_form['deck_name'],
                                 basic_optional_reversed_note_form['front'],
                                 basic_optional_reversed_note_form['back'],
                                 basic_optional_reversed_note_form['add_reverse'])
    return f.jsonify(True), 201


@app.route('/basic_type_in', methods=['POST'])
def create_basic_type_in_card():
    """ Creates a "Basic (type in the answer)"-modelled Anki card """
    basic_type_in_note_form = f.request.json
    basic_typein_note(basic_type_in_note_form['deck_name'],
                      basic_type_in_note_form['front'],
                      basic_type_in_note_form['back'])
    return f.jsonify(True), 201


@app.route('/cloze', methods=['POST'])
def create_cloze_card():
    """ Creates a "Cloze"-modelled Anki card """
    cloze_note_form = f.request.json
    cloze_note(cloze_note_form['deck_name'],
               cloze_note_form['sentence'],
               cloze_note_form['hidden_words'])
    return f.jsonify(True), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    Session.remove()
