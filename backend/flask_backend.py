import re

from flask import Flask, render_template, redirect, request, session
from db_access import DataBase
from graph_updater import update_graph
from threading import Thread
from data_provider import DataProvider
import socket
from food_controller import FoodController


app = Flask(__name__)
app.secret_key = 'hjewercv'
database = DataBase()
food_controller = None
data_provider = None


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        user = database.get_user(email, password)
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            session['privilege'] = user['privilege']
            return redirect('/monitor')
        else:
            return render_template('login.html', message='Wrong email or password(')
    return render_template('login.html', message="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        user_name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        is_account = database.is_account(email)
        if is_account:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not user_name or not password or not email:
            message = 'Please fill out the form !'
        else:
            database.add_account(user_name, email, password)
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message=message)


@app.route('/monitor')
def index():
    if 'loggedin' not in session or session['loggedin'] is not True:
        return redirect('/login')
    dataframe = database.get_all()
    update_graph(dataframe)
    cat_ratio = database.get_cat_ratio()
    filming_time = database.get_filming_time()
    time_from_last_cat = database.get_time_from_last_cat()
    statistic = {'cat_ratio': cat_ratio, 'filming_time': filming_time, 'time_from_last_cat': time_from_last_cat,
                 'feeding': food_controller.feeding, 'cat_present': data_provider.cat_present}
    return render_template('index.html', statistic=statistic)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect('/login')


@app.route('/feed/<int:on>', methods=['POST'])
def feed_control(on):
    if 'loggedin' in session and session['loggedin'] is True and session['privilege'] == 'admin':
        if on:
            food_controller.start_feeding()
        else:
            food_controller.stop_feeding()
    return redirect('/monitor')


if __name__ == '__main__':
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8200))
    server_socket.listen(0)
    # Accept a single connection and make a file-like object out of it
    print('Waiting for connection')
    connection_socket = server_socket.accept()[0]
    food_controller = FoodController(connection_socket)
    data_provider = DataProvider(connection_socket)
    Thread(target=data_provider.provide_data).start()
    app.run(debug=True, use_reloader=False)
