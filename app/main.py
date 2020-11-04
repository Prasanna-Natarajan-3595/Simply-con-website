# To run FLASK_APP=web_app/main.py flask run
from flask import Flask, render_template, session, request, redirect, url_for, flash
import psycopg2


app = Flask(__name__)
app.secret_key = 'aiohfoi83768403289fh;fh;df'
con = psycopg2.connect(database='d4mge65q9md3e0', user='rkmuneeusirhrx',
                       password='a189d2478896808847d963e639409b98adc3027f0ce3c7ecbbb0db5844f2fb9d', host='ec2-52-1-95-247.compute-1.amazonaws.com')

cur = con.cursor()
cur2 = con.cursor()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/me', methods=['POST', 'GET'])
def me():

        if not 'username' in session and not 'password' in session:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            if session['username'] == 'prasannanatarajan3595@gmail.com':
                if session['password'] == 'Prasanna@2005':
                    cur.execute("SELECT id, hostname, value, time FROM timing ORDER BY id")
                    cur2.execute("SELECT id, hostname, value, alt_value, send FROM sensor ORDER BY id")
                    return render_template('me.html', content=cur.fetchall(), content_2=cur2.fetchall())
                else:
                    flash('Wrong details')
                    return redirect(url_for('login'))
            else:
                flash('Wrong details')
                return redirect(url_for('login'))

        else:
            session.pop('username', None)
            session.pop('password', None)
            flash('Login in again')
            return redirect(url_for('login'))


@app.route('/me/timing/add')
def add():
    if 'username' in session and 'password' in session:
        if session['username'] == 'prasannanatarajan3595@gmail.com' and session['password'] == 'Prasanna@2005':
            return render_template('add.html')
    else:
        flash('First you need to be logged in')
        return redirect(url_for('login'))


@app.route('/me/timing/add/process', methods=['POST', 'GET'])
def process():
    if 'username' in session and 'password' in session:
        if session['username'] == 'prasannanatarajan3595@gmail.com' and session['password'] == 'Prasanna@2005':
            if request.method == 'POST':
                try:
                    cur.execute(f"INSERT INTO timing(hostname,value,time) VALUES('{request.form['host']}','{request.form['value']}',{request.form['time']})")
                    con.commit()
                    return redirect(url_for('me'))
                except Exception as e:
                    con.rollback()
                    flash(f'An error occured {e}')
                    return redirect(url_for('me'))
            else:

                return redirect(url_for('me'))
        else:
            flash('First you need to be logged in')
            return redirect(url_for('login'))
    else:
        flash('First you need to be logged in')
        return redirect(url_for('login'))


@app.route('/me/timing/<name>')
def remove_timing(name):
    name = int(name)
    try:
        cur.execute(f"DELETE FROM timing where id = {name} ")
        con.commit()
    except Exception as e:
        flash(f'An error occured {e}')
    return redirect(url_for('me'))


@app.route('/me/sensor/add')
def sensor_add():
    if 'username' in session and 'password' in session:
        if session['username'] == 'prasannanatarajan3595@gmail.com' and session['password'] == 'Prasanna@2005':
            return render_template('sensor_add.html')
    else:
        flash('First you need to be logged in')
        return redirect(url_for('login'))

@app.route('/me/sensor/add/process', methods=['POST', 'GET'])
def sensor_process():
    if 'username' in session and 'password' in session:
        if session['username'] == 'prasannanatarajan3595@gmail.com' and session['password'] == 'Prasanna@2005':
            if request.method == 'POST':
                try:
                    cur.execute(f"INSERT INTO sensor(hostname,value,alt_value,send) VALUES('{request.form['host']}','{request.form['value']}', '{request.form['alt_value']}','{request.form['send']}')")

                    con.commit()
                    return redirect(url_for('me'))
                except Exception as e:
                    con.rollback()
                    flash(f'An error occured {e}')
                    return redirect(url_for('me'))
            else:

                return redirect(url_for('me'))
        else:
            flash('First you need to be logged in')
            return redirect(url_for('login'))
    else:
        flash('First you need to be logged in')
        return redirect(url_for('login'))


@app.route('/me/sensor/<name>')
def remove_sensor(name):
    name = int(name)
    try:
        cur.execute(f"DELETE FROM sensor where id = {name} ")
        con.commit()
    except Exception as e:
        flash(f'An error occured {e}')
    return redirect(url_for('me'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))

