# To run FLASK_APP=web_app/main.py flask run
from flask import Flask, render_template, session, request, redirect, url_for, flash
import psycopg2

# Initializing all
app = Flask(__name__)
app.secret_key = 'aiohfoi83768403289fh;fh;df'
con = psycopg2.connect(database='simplycon', user='postgres',
                       password='2005', host='localhost')
cur = con.cursor()
cur2 = con.cursor()


# login page
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def loginsignup():
    return render_template('login_signup.html')


# Home page
@app.route('/me', methods=['POST', 'GET'])
def me():
    if not 'username' in session and not 'password' in session:
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        cur.execute("""SELECT id,name,email,password,timing_host,
                    timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send  FROM data ORDER BY id""")
        try:
            thing = [item for item in cur.fetchall()]
            thing2 = [item[2] for item in thing]  # Getting all emails
            if session['username'] in thing2:
                if thing[thing2.index(session['username'])][3] == session['password']:
                    cur.execute(f"""
                    SELECT id,name,email,password,timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send
                    FROM data
                    WHERE email='{session['username']}'
                    AND password='{session['password']}';
                    """)
                    val = cur.fetchall()
                    for i in val:
                        if i[2] == session['username']:
                            arr = []
                            for no,e in enumerate(i[4]):
                                arr.append([e,i[5][no],i[6][no]])

                    return render_template('me.html', content=arr)
                else:
                    flash('Wrong details')
                    return redirect(url_for('loginsignup'))
            else:
                flash('No users better signup')
                return redirect(url_for('signup'))
        except Exception as e:
            flash(f'An error occured {e}')
            return redirect(url_for('login'))
    else:
        session.pop('username', None)
        session.pop('password', None)
        flash('Login in again')
        return redirect(url_for('login'))


# timing add page
@app.route('/me/timing/add')
def add():
    try:
        cur.execute(
            'SELECT id, email, password, timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send FROM data ORDER BY id')
        thing = [item for item in cur.fetchall()]
        thing2 = [item[1] for item in thing]
        if session['username'] in thing2:

            if thing[thing2.index(session['username'])][2] == session['password']:
                return render_template('add.html')
            else:
                flash('Wrong details')
                return redirect(url_for('loginsignup'))
        else:
            flash('No users better signup')
            return redirect(url_for('signup'))
    except Exception as e:
        flash(f'An error occured {e}')
        return redirect(url_for('login'))


# timing add process page
@app.route('/me/timing/add/process', methods=['POST', 'GET'])
def process():
    if 'username' in session and 'password' in session:
        cur.execute(
            'SELECT id,email,password,timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send FROM data ORDER BY id')
        # try:
        thing = [item for item in cur.fetchall()]
        thing2 = [item[1] for item in thing]
        # try:
        if session['username'] in thing2:
            if thing[thing2.index(session['username'])][2] == session['password']:
                cur.execute(f"""
                        SELECT timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send
                        FROM data
                        WHERE email='{session['username']}'
                        AND password='{session['password']}';
                        """)
                val = cur.fetchall()
                if request.method == 'POST':
                    if val[0][0] == None:
                        cur.execute(f"""
                                update data 
                                set timing_host = ARRAY[ '{request.form['host']}' ]
                                where email='{session['username']}';""")
                        cur.execute(f"""
                                                                update data 
                                                                set timing_value = ARRAY[ '{request.form['value']}' ]
                                                                
                                                                where email='{session['username']}';""")
                        cur.execute(f"""
                                                                update data 
                                                                set 
                                                                timing_time = ARRAY[ {int(request.form['time'])} ]
                                                                where email='{session['username']}';""")
                        con.commit()
                        return redirect(url_for('me'))
                    else:
                        time_host = []
                        time_value = []
                        time_time = []
                        for i in val[0][0]:
                            time_host.append(i)
                        for i in val[0][1]:
                            time_value.append(i)
                        for i in val[0][2]:
                            time_time.append(i)
                        time_host.append(request.form['host'])
                        time_value.append(request.form['value'])
                        time_time.append(request.form['time'])

                        cur.execute(f"""update data
                                                set timing_host = ARRAY {time_host},
                                                timing_value = ARRAY {time_value},
                                                timing_time = ARRAY {time_time}
                                                where email='{session['username']}';""")
                        con.commit()
                        return redirect(url_for('me'))



                else:
                    flash('You need to be logged in')
                    return redirect(url_for('loginsignup'))

            else:
                flash('Wrong details')
                return redirect(url_for('loginsignup'))

    # except Exception as e:
    #         con.rollback()
    #         flash(f'An error occured {e}')
    #         return redirect(url_for('me'))
    # #except Exception as e:
    #     flash(f'An error occured {e}')
    #     return redirect(url_for('login'))
    else:
        flash('No users better signup')
        return redirect(url_for('signup'))


# timing delete page
@app.route('/me/timing/<name>')
def remove_timing(name):
    name = name.split(':')


    try:
        cur.execute(f"""
                                SELECT timing_host,timing_value,timing_time
                                FROM data
                                WHERE email='{session['username']}'
                                AND password='{session['password']}';
                                """)
        val = cur.fetchall()[0]
        return str(val)





    except Exception as e:
        flash(f'An error occured {e}')
    return redirect(url_for('me'))


# Sensor add page
@app.route('/me/sensor/add')
def sensor_add():
    if 'username' in session and 'password' in session:
        if session['username'] == 'prasannanatarajan3595@gmail.com' and session['password'] == 'Prasanna@2005':
            return render_template('sensor_add.html')
    else:
        flash('First you need to be logged in')
        return redirect(url_for('login'))


# Sensor add process page
@app.route('/me/sensor/add/process', methods=['POST', 'GET'])
def sensor_process():
    if 'username' in session and 'password' in session:
        if session['username'] == 'prasannanatarajan3595@gmail.com' and session['password'] == 'Prasanna@2005':
            if request.method == 'POST':
                try:
                    cur.execute(
                        f"INSERT INTO sensor(hostname,value,alt_value,send) VALUES('{request.form['host']}','{request.form['value']}', '{request.form['alt_value']}','{request.form['send']}')")

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
            return redirect(url_for('loginsignup'))
    else:
        flash('First you need to be logged in')
        return redirect(url_for('loginsignup'))


# Sensor delete page
@app.route('/me/sensor/<name>')
def remove_sensor(name):
    name = int(name)
    try:
        cur.execute(f"DELETE FROM sensor where id = {name} ")
        con.commit()
    except Exception as e:
        flash(f'An error occured {e}')
    return redirect(url_for('me'))


# Logout page
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    flash('Logged out successfully')
    return redirect(url_for('loginsignup'))


# Signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')


# Signup process page
@app.route('/signup/process', methods=['POST', 'GET'])
def signup_process():
    try:
        if request.method == 'POST':
            try:
                cur.execute('SELECT id, email, password FROM data ORDER BY id')
                if request.form['username'] in [item[1] for item in cur.fetchall()]:
                    flash('User already exist better login in')
                    return redirect(url_for('login'))
                else:
                    cur.execute(
                        f"INSERT INTO data(name,email,password) VALUES('{request.form['name']}','{request.form['username']}','{request.form['password']}')")
                    con.commit()
                    flash('Login again')
                    return redirect(url_for('login'))
            except Exception as e:
                flash(f'Got an error try again {e}')
                con.rollback()
                return redirect(url_for('signup'))
        else:
            flash('First you need to be sign up')
            return redirect(url_for('signup'))
    except Exception as e:
        flash(f'Got an error try again {e}')
        return redirect(url_for('signup'))


if __name__ == "__main__":
    app.run(debug=True)
