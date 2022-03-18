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
app.secret_key = 'se-team23'
app.config['MYSQL_HOST'] = db['mysql_hostname']
app.config['MYSQL_USER'] = db['mysql_username']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_database']

mysql = MySQL(app)

def mysql_connect():
    """MySQL python connection

    Returns:
        mysql.connection.cursor: Cursor for the connection
    """
    try:
        cursor = mysql.connection.cursor()
        return cursor
    except:
        return -1

def check_login_info(cur, table: str, username: str, password: str) -> Union[tuple, int]:
    """Check login info

    Args:
        cur (mysql.connection.cursor): MySQL cursor object
        table (str): which table to access
        username (str): username of the user
        password (str): password of the user
    Returns:
        Union[tuple, int]: _description_
    """

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
    except:
        return -1

def insert_visitor_login_info(cur, username: str, password: str, first_name: str, last_name: str, age: int, gender: str) -> int:
    """Function to insert visitor credentials to database

    Args:
        cur (mysql.connection.cursor): MySQL cursor object
        username (str): username of the user
        password (str): password of the user
        first_name (str): first name of the visitor
        last_name (str): last name of the visitor
        age (int): age of the visitor
        gender (str): gender of the visitor

    Returns:
        int: return code for the function
        0 for success
        -1 for error
        1062 for entering duplicate username
    """
    try:
        cur.execute("SELECT * FROM visitor WHERE username=%s;", (username,))
        info = cur.fetchone()
        if info is not None:
            return 1062
        cur.execute(
            'INSERT INTO visitor(username, pass, first_name, last_name, age, gender) VALUES("{username}", "{password}", "{first_name}", "{last_name}", {age}, "{gender}");'
            .format(username = username,
                    password = password,
                    first_name = first_name,
                    last_name = last_name,
                    age = age,
                    gender = gender))
        
    except:
        return -1
    mysql.connection.commit()
    return 0

def insert_place_login_info(cur, username: str, password: str, place_name: str, place_owner_full_name: str, place_address: str, place_postal_code: int) -> int:

    """Function to insert establishment owners credentials.

    Args:
        cur (mysql.connection.cursor): MySQL cursor object
        username (str): username of the user
        password (str): password of the user
        place_name (str): Name of the establishment
        place_owner_full_name (str): Establishment owner's full name
        place_address (str): last name of the visitor
        place_postal_code (int): postal code of the visitor

    Returns:
        int: return code for the function
        0 for success
        -1 for error
        1062 for entering duplicate username
    """
    try:
        cur.execute("SELECT * FROM place WHERE username=%s;", (username,))
        info = cur.fetchone()
        if info is not None:
            return 1062
        cur.execute(
            'INSERT INTO place(username, pass, place_name, place_owner_full_name, place_address, place_postal_code) VALUES("{username}", "{password}", "{place_name}", "{place_owner_full_name}", "{place_address}", "{place_postal_code}");'
            .format(username = username,
                    password = password,
                    place_name = place_name,
                    place_owner_full_name = place_owner_full_name,
                    place_address = place_address,
                    place_postal_code = place_postal_code))
        
    except:
        return -1
    mysql.connection.commit()
    return 0

#Below are the page rendering functions
def logout_page(**kwargs):
    url = "logout.html"
    return render_template(url, **kwargs)

def visitor_portal_page(**kwargs):
    url = "visitor_portal.html"
    return render_template(url, **kwargs)

def place_portal_page(**kwargs):
    url = "place_portal.html"
    return render_template(url, **kwargs)

def agent_portal_page(**kwargs):
    url = "agent_portal.html"
    return render_template(url, **kwargs)

def hospital_portal_page(**kwargs):
    url = "hospital_portal.html"
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

def registration_navigation_page(**kwargs):
    url = "registration_navigation.html"
    return render_template(url, **kwargs)



@app.route('/login', methods=['GET', 'POST'])
@auto.doc()
def login():
    """Login page backend

    Form Data: 
        username: Username
        password: Password
        user_type: Type of user (Visitor, Establishment owner, Agent, Hospital)
    If right credentials, redirects to portal.
    If invalid credentials, display an error message and retry.
    """
    try: 
        if session['is_logged_in'] and session['user_type']:
            if session['user_type'] ==  "visitor":
                return visitor_portal()
            elif session['user_type'] ==  "place":
                return place_portal()
            elif session['user_type'] ==  "agent":
                return agent_portal()
            elif session['user_type'] ==  "hospital":
                return hospital_portal()
    except:
        pass
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        cur = mysql_connect()
        if cur != -1:
            account_info = check_login_info(cur, user_type, username, password)
        else:
            return login_page(internal_server_error=True)
        if account_info != -1:
            if account_info:
                if user_type == "visitor":
                    session['is_logged_in'] = True
                    session['user_type'] = user_type
                    session['username'] = username
                    session['user_id'] = account_info[0]
                    session['visitor_first_name'] = account_info[3]
                    session['visitor_last_name'] = account_info[4]
                    cur.close()
                    return visitor_portal()
                elif user_type == "place":
                    session['is_logged_in'] = True
                    session['user_type'] = user_type
                    session['username'] = username
                    session['user_id'] = account_info[0]
                    session['place_name'] = account_info[3]
                    session['place_owner_full_name'] = account_info[4]
                    cur.close()
                    return place_portal()
                elif user_type == "agent":
                    session['is_logged_in'] = True
                    session['user_type'] = user_type
                    session['username'] = username
                    session['user_id'] = account_info[0]
                    session['agent_full_name'] = account_info[3]
                    cur.close()
                    return agent_portal()
                elif user_type == "hospital":
                    
                    session['is_logged_in'] = True
                    session['user_type'] = user_type
                    session['username'] = username
                    session['user_id'] = account_info[0]
                    session['hospital_name'] = account_info[3]
                    session['hospital_medical_id'] = account_info[4]
                    cur.close()
                    return hospital_portal()
            else:
                cur.close()
                return login_page(invalid_credentials=True)
        else:
            cur.close()
            return login_page(internal_server_error=True)
        
    else:
        return login_page()
    



@app.route('/visitor_portal', methods=['GET'])
@auto.doc()
def visitor_portal():
    """Visitor portal backend

    Content:
        Here visitor can start the QR code of different establishment notifying there presence
    """
    try:
        if session['is_logged_in'] == True and session['user_type'] == "visitor":
            return visitor_portal_page(username = session['username'],
                                first_name = session['visitor_first_name'],
                                last_name = session['visitor_last_name'],
                                visitor_id = session['user_id'])
        else:
            return login_page()
    except:
        return login_page()

@app.route('/agent_portal', methods=['GET'])
@auto.doc()
def agent_portal():
    """Agent portal backend

    Content:
        Portal page for the agent
        Here agent can monitor the visitor tracking and download data 
    """
    try:
        if session['is_logged_in'] == True and session['user_type'] == "agent":
            return agent_portal_page(username = session['username'],
                                agent_full_name = session['agent_full_name'],
                                agent_id = session['user_id'])
        else:
            return login_page()
    except:
        return login_page()

@app.route('/hospital_portal', methods=['GET'])
@auto.doc()
def hospital_portal():
    """Hospital portal backend

    Content:
        Portal page for the hospital
        Here hospital can upload the visitors test reports
    """
    try:
        if session['is_logged_in'] == True and session['user_type'] == "hospital":
            return hospital_portal_page(username = session['username'],
                                hospital_name = session['hospital_name'],
                                user_id = session['user_id'],
                                hospital_medical_id = session['hospital_medical_id'])
        else:
            return login_page()
    except:
        return login_page()




@app.route('/place_portal', methods=['GET'])
@auto.doc()
def place_portal():
    """Place portal backend

    Content:
        Here establishment owner can check who arrived at their establishment and allow visitors to enter
    """
    try:
        if session['is_logged_in'] == True and session['user_type'] == "place":
            return place_portal_page(username = session['username'],
                                place_name = session['place_name'],
                                place_owner_full_name = session['place_owner_full_name'],
                                place_id = session['user_id'])
        else:
            return login_page()
    except:
        return login_page()
   

@app.route('/logout', methods=['GET'])
@auto.doc()
def logout():
    """Logout Page Back end

    Content:
        Here a user can either login again or go back to index page.
    """
    session.clear()
    return logout_page(logout_success = True)


@app.route('/visitor_registration', methods=['GET', 'POST'])
@auto.doc()
def visitor_registration():
    """Visitor resgistration backend

    Form:
        Here visitor can set their new username, password, and their demographics.
        In case of password mismatch or duplicate username, visitor have to retry again with
        proper credentials
    """
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
        if int(age) > 120 or int(age) < 0:
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
                elif err == -1:
                    internal_server_error_flag = True
            cur.close()
        if not internal_server_error_flag and not dup_user_flag and not age_flag and not confirm_password_flag:
            success_registration_flag  = True
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
    """Place resgistration backend

    Form:
        Here establishment owners can set their new username, password, and the information about their establishement.
        In case of password mismatch or duplicate username, establishment owners have to retry again with
        proper credentials.
    """
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
                elif err == -1:
                    internal_server_error_flag = True
            cur.close()
        if not internal_server_error_flag and not dup_user_flag and not confirm_password_flag:
            success_registration_flag  = True
        return place_registration_page(success_registration=success_registration_flag,
                                     internal_server_error = internal_server_error_flag,
                                     dup_user_error = dup_user_flag,
                                     confirm_password_error = confirm_password_flag)
    else:
        return place_registration_page()


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    """Index page backend

    Content:
        Here users can go to login or registration page
    """
    return index_page()

@app.route('/registration_navigation', methods=['POST', 'GET'])
def registration_navigation():
    """Registration navigation backend

    Content:
        Navigate between visitor or establishemnt owner registration page
    """
    return registration_navigation_page()

@app.route('/docs')
def documentation():
    return auto.html(title='Corona Archive API documentation')

if __name__ == '__main__':
    app.run(debug=True)
