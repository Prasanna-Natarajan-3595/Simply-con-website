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


# login with signup button
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
                            if i[4] == None:
                                arr = []
                                break
                            else:
                                arr = []
                                for no, e in enumerate(i[4]):
                                    arr.append([no, e, i[5][no], i[6][no]])
                    for e in val:
                        if e[2] == session['username']:
                            if e[7] == None:
                                arrs = []
                                break
                            else:
                                arrs = []
                                for no, f in enumerate(e[7]):
                                    arrs.append([no, f, e[8][no], e[9][no], e[10][no]])
                    cur.execute(f"""
                                        SELECT id,name,email,password,timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send
                                        FROM data
                                        WHERE email='{session['username']}'
                                        AND password='{session['password']}';
                                        """)
                    val = cur.fetchall()

                    return render_template('me.html', content=arr, content_2=arrs, name=val[0][1])
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

        thing = [item for item in cur.fetchall()]
        thing2 = [item[1] for item in thing]
        try:
            if session['username'] in thing2:
                if thing[thing2.index(session['username'])][2] == session['password']:
                    cur.execute(f"""
                        SELECT timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send
                        FROM data
                        WHERE email='{session['username']}'
                        AND password='{session['password']}';
                        """)
                    val = cur.fetchall()
                    try:
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
                                time_time.append(int(request.form['time']))

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
                    except Exception as e:
                        con.rollback()
                        flash(f'An error occured {e}')
                        return redirect(url_for('me'))

                else:
                    flash('Wrong details')
                    return redirect(url_for('loginsignup'))

        except Exception as e:
            con.rollback()
            flash(f'An error occured {e}')
            return redirect(url_for('me'))

    else:
        flash('No users better signup')
        return redirect(url_for('signup'))


# timing delete page
@app.route('/me/timing/<name>')
def remove_timing(name):
    name = int(name)

    try:
        cur.execute(f"""
                                SELECT timing_host,timing_value,timing_time
                                FROM data
                                WHERE email='{session['username']}'
                                AND password='{session['password']}';
                                """)

        val = cur.fetchall()[0]
        if val[0] == None:
            arrs = []

        else:
            arrs = []
            for no, f in enumerate(val[0]):
                arrs.append([no, f, val[1][no], val[2][no]])
        for i in arrs:
            if name == i[0]:
                arrs.remove(i)
        time_host = []
        time_value = []
        time_time = []
        for s in arrs:
            time_host.append(s[1])
            time_value.append(s[2])
            time_time.append(s[3])
        if time_host == []:
            cur.execute(f"""update data
                                                                    set timing_host = ARRAY []::varchar[],
                                                                    timing_value = ARRAY []::varchar[],
                                                                    timing_time = ARRAY []::integer[]
                                                                    where email='{session['username']}';""")
            con.commit()
        else:
            cur.execute(f"""update data
                                                        set timing_host = ARRAY {time_host},
                                                        timing_value = ARRAY {time_value},
                                                        timing_time = ARRAY {time_time}
                                                        where email='{session['username']}';""")
            con.commit()
            return redirect(url_for('me'))





    except Exception as e:
        flash(f'An error occured {e}')
    return redirect(url_for('me'))


# Sensor add page
@app.route('/me/sensor/add')
def sensor_add():
    try:
        cur.execute(
            'SELECT id, email, password, timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send FROM data ORDER BY id')
        thing = [item for item in cur.fetchall()]
        thing2 = [item[1] for item in thing]
        if session['username'] in thing2:

            if thing[thing2.index(session['username'])][2] == session['password']:
                return render_template('sensor_add.html')
            else:
                flash('Wrong details')
                return redirect(url_for('loginsignup'))
        else:
            flash('No users better signup')
            return redirect(url_for('signup'))
    except Exception as e:
        flash(f'An error occured {e}')
        return redirect(url_for('login'))


# Sensor add process page
@app.route('/me/sensor/add/process', methods=['POST', 'GET'])
def sensor_process():
    if 'username' in session and 'password' in session:
        cur.execute(
            'SELECT id,email,password,timing_host,timing_value,timing_time,sensor_host,sensor_value,sensor_alt,sensor_send FROM data ORDER BY id')

        thing = [item for item in cur.fetchall()]
        thing2 = [item[1] for item in thing]
        try:
            if session['username'] in thing2:
                if thing[thing2.index(session['username'])][2] == session['password']:
                    cur.execute(f"""
                        SELECT sensor_host,sensor_value,sensor_alt,sensor_send
                        FROM data
                        WHERE email='{session['username']}'
                        AND password='{session['password']}';
                        """)
                    val = cur.fetchall()
                    try:
                        if request.method == 'POST':
                            if val[0][0] == None:
                                cur.execute(f"""
                                update data 
                                set sensor_host = ARRAY[ '{request.form['host']}' ]
                                where email='{session['username']}';""")
                                cur.execute(f"""
                                                                update data 
                                                                set sensor_value = ARRAY[ '{request.form['value']}' ]

                                                                where email='{session['username']}';""")
                                cur.execute(f"""
                                                 update data 
                                                 set sensor_host = ARRAY[ '{request.form['host']}' ]
                                                 where email='{session['username']}';""")
                                cur.execute(f"""
                                                                update data 
                                                                set 
                                                                sensor_alt = ARRAY[ '{request.form['alt_value']}' ]
                                                                where email='{session['username']}';""")
                                cur.execute(f"""
                                                                                                update data 
                                                                                                set 
                                                                                                sensor_send = ARRAY[ '{request.form['send']}' ]
                                                                                                where email='{session['username']}';""")
                                con.commit()
                                return redirect(url_for('me'))
                            else:
                                sensor_host = []
                                sensor_value = []
                                sensor_altvalue = []
                                sensor_send = []
                                for i in val[0][0]:
                                    sensor_host.append(i)
                                for i in val[0][1]:
                                    sensor_value.append(i)
                                for i in val[0][2]:
                                    sensor_altvalue.append(i)
                                for i in val[0][3]:
                                    sensor_altvalue.append(i)
                                sensor_host.append(request.form['host'])
                                sensor_value.append(request.form['value'])
                                sensor_altvalue.append(request.form['alt_value'])
                                sensor_send.append(request.form['send'])

                                cur.execute(f"""update data
                                                set sensor_host = ARRAY {sensor_host},
                                                sensor_value = ARRAY {sensor_value},
                                                sensor_altvalue = ARRAY {sensor_altvalue},
                                                sensor_send = ARRAY {sensor_send}
                                                where email='{session['username']}';""")
                                con.commit()
                                return redirect(url_for('me'))



                        else:
                            flash('You need to be logged in')
                            return redirect(url_for('loginsignup'))
                    except Exception as e:
                        con.rollback()
                        flash(f'An error occured {e}')
                        return redirect(url_for('login'))
                else:
                    flash('Wrong details')
                    return redirect(url_for('loginsignup'))

        except Exception as e:
            con.rollback()
            flash(f'An error occured {e}')
            return redirect(url_for('me'))

    else:
        flash('No users better signup')
        return redirect(url_for('signup'))


# Sensor delete page
@app.route('/me/sensor/<name>')
def remove_sensor(name):
    name = int(name)

    try:
        cur.execute(f"""
                                    SELECT sensor_host,sensor_value,sensor_alt,sensor_send
                                    FROM data
                                    WHERE email='{session['username']}'
                                    AND password='{session['password']}';
                                    """)

        val = cur.fetchall()[0]
        if val[0] == None:
            arrs = []

        else:
            arrs = []
            for no, f in enumerate(val[0]):
                arrs.append([no, f, val[1][no], val[2][no], val[3][no]])
        for i in arrs:
            if name == i[0]:
                arrs.remove(i)
        sensor_host = []
        sensor_value = []
        sensor_alt = []
        sensor_send = []
        for s in arrs:
            sensor_host.append(s[1])
            sensor_value.append(s[2])
            sensor_alt.append(s[3])
            sensor_send.append(s[4])
        if sensor_host == []:
            cur.execute(f"""update data
                                                                        set sensor_host = ARRAY []::varchar[],
                                                                        sensor_value = ARRAY []::varchar[],
                                                                        sensor_alt = ARRAY []::varchar[],
                                                                        sensor_send = ARRAY []::varchar[]
                                                                        where email='{session['username']}';""")
            con.commit()
        else:
            cur.execute(f"""update data
                                                            set sensor_host = ARRAY {sensor_host},
                                                            sensor_value = ARRAY {sensor_value},
                                                            sensor_alt = ARRAY {sensor_alt},
                                                            sensor_send = ARRAY {sensor_send}
                                                            where email='{session['username']}';""")
            con.commit()
            return redirect(url_for('me'))





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


# Profile page
@app.route('/me/profile')
def profile():
    cur.execute(f"""SELECT name
                                FROM data
                                WHERE email='{session['username']}'
                                AND password='{session['password']}';""")
    v = cur.fetchall()
    return render_template('profile.html',name=v[0][0],email=session['username'],password=session['password'])


# Profile page saver
@app.route('/me/profile/save', methods=['POST','GET'])
def profile_save():
    if request.method == 'POST':
        if 'username' in session and 'password' in session:
            cur.execute(f"""
                           update data 
                           set name = '{request.form['name']}'
                           where email='{session['username']}';""")
            cur.execute(f"""
                                                        update data 
                                                        set password = '{request.form['password']}'
                                                        where email='{session['username']}';""")
            con.commit()

            return redirect(url_for('me'))
        else:
            flash('First you need to be logged in ')
            return redirect(url_for('login'))
    else:
        flash('First you need to be logged in ')
        return redirect(url_for('login'))


# Deletes your account
@app.route('/delete')
def delete():
    if 'username' in session and 'password' in session:
        cur.execute(f"""DELETE FROM data
                        WHERE email='{session['username']}';""")
        con.commit()
        return redirect(url_for('loginsignup'))


# This is help page
@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)
