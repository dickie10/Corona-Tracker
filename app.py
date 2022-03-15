from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime
from flask_selfdoc import Autodoc
import yaml
import os
from typing import List, Tuple, Union

app = Flask(__name__)
auto = Autodoc(app)

db = yaml.safe_load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_hostname']
app.config['MYSQL_USER'] = db['mysql_username']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_database']

mysql = MySQL(app)

def mysql_connect():
    try:
        cursor = mysql.connection.cursor()
        return cursor
    except (MySQL.Error, MySQL.Warning) as e:
        return e.args[0]

def check_login_info(cur, table, username, password) -> Union[tuple, int]:
    try:
        if table == "visitor":
            cur.execute('SELECT *  FROM visitor WHERE username = "{username}" AND pass = "{password}";'
                        .format(username = username, password = password))
        elif table == "place":
            cur.execute('SELECT *  FROM place WHERE username = "{username}" AND pass = "{password}";'
                        .format(username = username, password = password))
        elif table == "agent":
            cur.execute('SELECT *  FROM agent WHERE username = "{username}" AND pass = "{password}";'
                        .format(username = username, password = password))
        elif table == "hospital":
            cur.execute('SELECT *  FROM hospital WHERE username = "{username}" AND pass = "{password}";'
                        .format(username = username, password = password))
            
        m = cur.fetchone()
        return m
    except (mysql.Error, mysql.Warning) as e:
        return e.args[0]

def insert_place_login_info(cur, username, password, place_name, place_owner_full_name, place_address, place_postal_code) -> int:
    try:
        cur.execute(
            'INSERT INTO visitor(username, pass) VALUES("{username}", "{password}");'
            .format(username = username, password = password))
    except (mysql.Error, mysql.Warning) as e:
        return e.args[0]
    con.commit()
    return 0


def logout_page(**kwargs):
    url = "logout.html"
    return render_template(url, **kwargs)

def visitor_portal_page(**kwargs):
    url = "visitor_portal.html"
    return render_template(url, **kwargs)

def place_portal_page(**kwargs):
    url = "place_portal.html"
    return render_template(url, **kwargs)

def index_page(**kwargs):
    url = "index.html"
    return render_template(url, **kwargs)

def login_page(**kwargs):
    url = "login.html"
    return render_template(url, **kwargs)

def visitor_registration_page(**kwargs):
    url = "visitor_registration.html"
    return render_template(url, **kwargs)
    
def place_registration_page(**kwargs):
    url = "place_registration.html"
    return render_template(url, **kwargs)

@app.route('/login', methods=['GET', 'POST'])
@auto.doc()
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        cur = mysql_connect()
        if type(cur) != "int":
            account_info = check_login_info(cur, user_type, username, password)
        if type(account_info) != "int":
            if account_info:
                if user_type == "visitor":
                    session['is_logged_in'] = True
                    session['user_type'] = user_type
                    session['username'] = username
                    session['user_id'] = account_info[0]
                    session['visitor_first_name'] = account_info[1]
                    session['visitor_last_name'] = account_info[2]
                    cur.close()
                    return visitor_portal()
                elif user_type == "place":
                    session['is_logged_in'] = True
                    session['user_type'] = user_type
                    session['username'] = username
                    session['user_id'] = account_info[0]
                    session['place_name'] = account_info[1]
                    session['place_owner_full_name'] = account_info[2]
                    cur.close()
                    return visitor_portal()
            else:
                cur.close()
                return login_page(invalid_credentials=True)
    else:
        return login_page()
    
@app.route('/visitor_registration', methods=['GET', 'POST'])
@auto.doc()
def visitor_registration():
    if request.method == 'POST':
        commit_flag = True
        age_flag = False
        confirm_password_flag = False
        dup_user_flag = False
        internal_server_error_flag = False
        success_registration_flag = False
        register_credentials = request.form
        username = register_credentials["username"]
        password = register_credentials["password"]
        confirm_password = register_credentials["confirm_password"]
        first_name = register_credentials["first_name"]
        last_name = register_credentials["last_name"]
        age = register_credentials["age"]
        gender = register_credentials["gender"]
        if age > 120 or age < 0:
            commit_flag = False
            age_flag = True
        if password != confirm_password:
            commit_flag = False
            confirm_password_flag = True
        if commit_flag:
            cur = mysql_connect()
            err = insert_visitor_login_info(cur, username, password, first_name, last_name, age, gender)
            if err != 0:
                if err == 1062:
                    dup_user_flag = True
                else:
                    internal_server_error_flag = True
            cur.close()
            return visitor_registration_page(success_registration=success_registration_flag,
                                     internal_server_error = internal_server_error_flag,
                                     dup_user_error = dup_user_flag,
                                     age_error = age_flag,
                                     confirm_password_error = confirm_password_flag)
    else:
        return visitor_registration_page()

@app.route('/place_registration', methods=['GET', 'POST'])
@auto.doc()
def place_registration():
    if request.method == 'POST':
        commit_flag = True
        confirm_password_flag = False
        dup_user_flag = False
        internal_server_error_flag = False
        success_registration_flag = False
        register_credentials = request.form
        username = register_credentials["username"]
        password = register_credentials["password"]
        confirm_password = register_credentials["confirm_password"]
        place_name = register_credentials["place_name"]
        place_owner_full_name = register_credentials["place_owner_full_name"]
        place_address = register_credentials["place_address"]
        place_postal_code = register_credentials["place_postal_code"]
        if password != confirm_password:
            commit_flag = False
            confirm_password_flag = True
        if commit_flag:
            cur = mysql_connect()
            err = insert_place_login_info(cur, username, password, place_name, place_owner_full_name, place_address, place_postal_code)
            if err != 0:
                if err == 1062:
                    dup_user_flag = True
                else:
                    internal_server_error_flag = True
            cur.close()
            return place_registration_page(success_registration=success_registration_flag,
                                     internal_server_error = internal_server_error_flag,
                                     dup_user_error = dup_user_flag,
                                     confirm_password_error = confirm_password_flag)
    else:
        return place_registration_page()


@app.route('/visitor_portal', methods=['GET', 'POST'])
@auto.doc()
def visitor_portal():
    try:
        if session['is_logged_in'] and session['user_type'] == "visitor":
            return visitor_portal_page(username = session['username'],
                                first_name = session['visitor_first_name'],
                                last_name = session['visitor_last_name'],
                                visitor_id = session['user_id'])
        else:
            return login_page()
    except:
        return login_page()

@app.route('/place_portal', methods=['GET', 'POST'])
@auto.doc()
def place_portal():
    try:
        if session['is_logged_in'] and session['user_type'] == "place":
            return place_portal_page(username = session['username'],
                                place_name = session['place_first_name'],
                                place_owner_full_name = session['place_last_name'],
                                place_id = session['user_id'])
        else:
            return login_page()
    except:
        return login_page()

@app.route('/logout', methods=['GET', 'POST'])
@auto.doc()
def logout():
    session.clear()
    return logout_page()


'''
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
'''

@app.route('/', methods=['POST', 'GET'])
def index():
    return index_page()

'''
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
'''

'''
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['data']
        task.date_created = datetime.utcnow()
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html', task=task)
'''

if __name__ == '__main__':
    app.run(debug=True)
