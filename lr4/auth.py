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


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if not username or not password:
        # flash('Input login or password', 'error')
        return render_template('login.html', error='Input login or password')
    elif not records:
        flash('Your login or password was incorrect', 'error')
        return render_template('login.html')
    else:
        return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
