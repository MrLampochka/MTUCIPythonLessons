import requests
from flask import Flask, render_template, request, flash, redirect, url_for
import psycopg2

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='very_secret_key'
)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="123123",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

DATA = {
    'username': '',
    'password': '',
    'records': [],
}


@app.route('/login/', methods=['POST'])
def login_post():
    # if request.form.get("login"):
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if not username or not password:
        # flash('Input login or password', 'error')
        return render_template('login.html', error='Input login or password')
    elif not records:
        return render_template('login.html', error='Your login or password was incorrect')
    else:
        DATA['username'] = username
        DATA['password'] = password
        DATA['records'] = records
        return redirect(url_for('account'))

    # elif request.form.get("registration"):
    #     return redirect("/registration/")


@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute(f"SELECT * FROM service.users WHERE login='{str(login)}';")
        # проверка на существование аккаунта
        if cursor.fetchall():
            return render_template('registration.html', error='Account already exists')

        if name and login and password:
            if password == request.form.get('con-password'):
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES ( %s, %s, %s);', (str(name), str(login), str(password)))
                conn.commit()
                return redirect('/successful/')
            else:
                return render_template('registration.html', error='Passwords do not match')
        else:
            return render_template('registration.html', error='Fill in all fields correctly')
    return render_template('registration.html')


@app.route('/account/', methods=['POST', 'GET'])
def account():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        return render_template('account.html', full_name=DATA['records'][0][1], login=DATA['records'][0][2],
                               password=DATA['records'][0][3])

@app.route('/successful/', methods=['POST', 'GET'])
def successful():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        return render_template('successful.html')


if __name__ == "__main__":
    app.run(debug=True)
