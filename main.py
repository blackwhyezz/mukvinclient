from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


# Load users from JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    else:
        return []


# Save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)


# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = load_users()
        existing_user = next((user for user in users if user['username'] == username), None)

        if existing_user:
            return redirect(url_for('register'))

        new_user = {
            'id': len(users) + 1,
            'username': username,
            'email': email,
            'password': password,
            'rol': 'Пользыватель',
            'hwid': '125adc234dfag',
            'licence': 'Купи уже ее пидор',
            'regdate': datetime.now().strftime('%d.%m.%Y | %H:%M')
        }

        users.append(new_user)
        save_users(users)

        return redirect(url_for('login'))

    return render_template('register.html')


# Login an existing user
global pidor


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('user_panel'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)

        if user:
            session['logged_in'] = True
            session['userdata'] = user
            if user['rol'] == 'Admin':
                return redirect(url_for('admin_panel'))  # Redirect to user_panel.htm
            else:
                return redirect(url_for('user_panel'))  # Redirect to user_panel.html
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/user_panel')
def user_panel():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('user_panel.html', user=session['userdata']['username'], id=session['userdata']['id'],
                           mail=session['userdata']['email'], prezik=session['userdata']['regdate'],
                           rol=session['userdata']['rol'], hwid=session['userdata']['hwid'],
                           licence=session['userdata']['licence'])


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))


@app.route('/admin_panel')
def admin_panel():
    if session['userdata']['rol'] != 'Admin':
        users = load_users()
        if 'logged_in' not in session:
            loggedl = 'Войти / Зарегистрироваться'
        else:
            loggedl = 'Личный кабинет'
        return render_template('index.html', member=len(users), cabinetlabel=loggedl)

    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('admin_panel.html', user=session['userdata']['username'], id=session['userdata']['id'],
                           mail=session['userdata']['email'], prezik=session['userdata']['regdate'],
                           rol=session['userdata']['rol'], hwid=session['userdata']['hwid'],
                           licence=session['userdata']['licence'])


@app.route('/')
def index():
    users = load_users()
    if 'logged_in' not in session:
        loggedl = 'Войти / Зарегистрироваться'
    else:
        loggedl = 'Личный кабинет'
    return render_template('index.html', member=len(users), cabinetlabel=loggedl)


if __name__ == '__main__':
    app.run(debug=True)
