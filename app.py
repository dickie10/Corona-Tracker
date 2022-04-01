from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime
from flask_selfdoc import Autodoc
import yaml 
import qrcode 
import os
from typing import List, Tuple, Union
import json
from datetime import date

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
    
    cursor = mysql.connection.cursor()
    return cursor
    

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

def insert_visitor_login_info(cur, username: str, password: str, first_name: str, last_name: str, age: int, gender: str,infected: int, address: str, email: str, phonenumber: str) -> int:
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
    
    print("in try")
    cur.execute("SELECT * FROM visitor WHERE username=%s;", (username,))
    info = cur.fetchone()
    if info is not None:
        return 1062 
    try:
        cur.execute(
            'INSERT INTO visitor(username, pass, first_name, last_name, age, gender,infected,address,email,phonenumber) VALUES("{username}", "{password}", "{first_name}", "{last_name}", "{age}", "{gender}", "{infected}" , "{address}" ,"{email}", "{phonenumber}");'
            .format(username = username,
                    password = password,
                    first_name = first_name,
                    last_name = last_name,
                    age = age,
                    gender = gender, 
                    infected = infected,
                    address=address,
                    email=email,
                    phonenumber=phonenumber))
    except:
        return -1    
    mysql.connection.commit()
    return 0

def insert_place_login_info(cur, username: str, password: str, place_name: str, place_owner_full_name: str, place_address: str, place_postal_code: int, word: str) -> int:

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
            'INSERT INTO place(username, pass, place_name, place_owner_full_name, place_address, place_postal_code,QRcode) VALUES("{username}", "{password}", "{place_name}", "{place_owner_full_name}", "{place_address}", "{place_postal_code}","{word}");'
            .format(username = username,
                    password = password,
                    place_name = place_name,
                    place_owner_full_name = place_owner_full_name,
                    place_address = place_address,
                    place_postal_code = place_postal_code,
                    word = word))
        
    except:
        return -1
    mysql.connection.commit()
    return 0

#Below are the page rendering functions
def logout_page(**kwargs):
    url = "logout.html"
    return render_template(url, **kwargs)

def visitor_portal_page(**kwargs):
    return render_template("scancam.html")

def place_portal_page(**kwargs):  
    return render_template("qrgen.html")

def agent_portal_page(**kwargs):
    return render_template("agent_portal.html")

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

def agent_add_hospital(**kwargs): 
    url = "addhospital.html" 
    return render_template(url, **kwargs)

def loged_into_place_page(**kwargs):
    url = "logedIntoPlace.html"
    return render_template(url, **kwargs)


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
@auto.doc()
def index():
    """Index page backend

    Content:
        Here users can go to login or registration page
    """
    return index_page()

@app.route('/login', methods=['GET', 'POST'])
@auto.doc()
def login():
    print("in login")
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
            print("here")
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
    

@app.route('/insert_agent_hospital', methods=['GET', 'POST']) 
def insert_agent_hospital(cur,vist_name: str,vist_password: str,vist_hosp_name,vist_hosp_id): 
    try:
        cur.execute("SELECT * FROM hospital WHERE username=%s;", (vist_name,)) 
        info = cur.fetchone()  
        if info is not None:
            return 1062 
        cur.execute("SELECT * FROM hospital WHERE hospital_medical_id=%s;", (vist_hosp_id,)) 
        info2 = cur.fetchone() 
        if info2 is not None: 
            return 1063 
        cur.execute(
                'INSERT INTO hospital(username, pass, hospital_name, hospital_medical_id) VALUES("{vist_name}", "{vist_password}", "{vist_hosp_name}", "{vist_hosp_id}");'
                .format(vist_name = vist_name,
                        vist_password = vist_password,
                        vist_hosp_name = vist_hosp_name,
                        vist_hosp_id = vist_hosp_id))
    except:
        return -1
    mysql.connection.commit() 
    return 0 

@app.route('/visitor_portal', methods=['GET', 'POST'])
@auto.doc()
def visitor_portal():

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

@app.route('/read_qr_code', methods = ['POST'])
@auto.doc()
def read_qr_code():
    try:
        print("here")
        if session['is_logged_in'] == True and session['user_type'] == "visitor":
            print(request.method)
            print(request.form)
            code = request.form["input"]
            print("The system received code:")
            print(code)

            #Creating the sql call to find the place associated with the just received code
            sql_select_from_place = f"SELECT user_id, place_name from place WHERE QRcode='{code}';"   
            con = mysql_connect() 
            con.execute(sql_select_from_place)
            data = con.fetchall() 
            #preparing the data for the insertion call
            place_id = data[0][0]
            place_name = data[0][1]
            user_id = session['user_id'] 
            #getting the current time and date 
            arrival_time = getCurrentDateAndTime()
            #logging the information for debuging
            print("The current information which witch the user has loged into the place is:")
            print("The place id is:")
            print(place_id)
            print("The place_name is")
            print(place_name)
            print("The user_id is")
            print(user_id)
            print("The arrival_time is")
            print(arrival_time)

            #insertion call
            
            try:
                con = mysql_connect()
                sqlInsertIntoPlace = 'INSERT INTO visitedPlace(user_id, place_id,arrival_time) VALUES({user_id}, {place_id},"{arrival_time}");'.format(user_id = user_id,place_id = place_id,arrival_time = arrival_time)

                print(sqlInsertIntoPlace)
                con.execute(sqlInsertIntoPlace)
            except:
                print("failed to connect to the database please try again later")
                return "failed to connect to the database please try again later"
            
            print("the id of the last inserted element is:")
            print(con.lastrowid)
            session["curent_Visit_Id"] = con.lastrowid
            mysql.connection.commit()
            return redirect("/logedIntoPlace/"+place_name)
        else:
            return login_page()
    except:
        return render_template("erroecodepage.html")

def getCurrentDateAndTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y") 
    dt2_string = now.strftime("%H:%M:%S") 
    val_string = str(dt_string)+str(" ")+str(dt2_string)
    return val_string

@app.route('/logedIntoPlace/<place_name>', methods=['GET'])
@auto.doc()
def logedIntoPlace(place_name):
    if request.method == 'GET':
        try:
            print("in logedIntoPlace")
            if session['is_logged_in'] == True and session['user_type'] == "visitor":
                print("before login_page()")
                return loged_into_place_page(username = session['username'],
                                    first_name = session['visitor_first_name'],
                                    last_name = session['visitor_last_name'],
                                    visitor_id = session['user_id'],
                                    currentlyVisitingPlace_id = session['curent_Visit_Id'],
                                    placeName = place_name)
            else:
                return login_page()
        except:
            return login_page()


@app.route('/exitPlace', methods=['POST'])
@auto.doc()
def exitPlace():
    
    print("you are thereby exiting your place this entry has the id;")
    print(session['curent_Visit_Id'])
    leaveTime = getCurrentDateAndTime()
    visit_id = session['curent_Visit_Id']
    try:
        con = mysql_connect()
        sql_update_visitedPlace = 'update visitedPlace set leave_time = "{leaveTime}" where visit_id = {visit_id}'.format(leaveTime = leaveTime, visit_id = visit_id)
        print(sql_update_visitedPlace)
        con.execute(sql_update_visitedPlace)
    except:
        print("something went wrong")
        return login_page()

    mysql.connection.commit()

    return visitor_portal_page(username = session['username'],
                                first_name = session['visitor_first_name'],
                                last_name = session['visitor_last_name'],
                                visitor_id = session['user_id'])

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
            cur = mysql_connect()
            cur.execute("SELECT QRcode FROM place WHERE username=%s;", (session['username'],)) 
            value = cur.fetchone()  
            img = qrcode.make(value) #qr code generated 
            img.save("./static/img/trail.jpg")
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
@app.route('/addhospital', methods=['GET']) 
def addhospital(): 
    return render_template('addhospital.html') 
@app.route('/Display', methods=['GET']) 
def Display(): 
     cur = mysql_connect() 
     cur.execute("SELECT * from visitedPlace") 
     data =  cur.fetchall() 
     if len(data) != 0: 
          return render_template("Displayvisitors.html", value=data) 
     else: 
           return render_template()

@app.route('/visitor_registration', methods=['GET', 'POST'])
@auto.doc()
def visitor_registration():
    """Visitor resgistration backend

    Form:
        Here visitor can set their new username, password, and their demographics.
        In case of password mismatch or duplicate username, visitor have to retry again with
        proper credentials
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
        address = register_credentials["address"] 
        email = register_credentials["email"]  
        infected = 0 
        phonenumber = register_credentials["phonenumber"] 
        print("before the commit")
        if int(age) > 120 or int(age) < 0:
            commit_flag = False
            age_flag = True
        if password != confirm_password:
            commit_flag = False
            confirm_password_flag = True
        if commit_flag: 
            print("sql connected")
            cur = mysql_connect()
            err = insert_visitor_login_info(cur, username, password, first_name, last_name, age, gender,infected,address,email,phonenumber) 
            print("after err")
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

    if request.method == 'POST': 
        word = ""
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
            word = str(username) + str(place_name) + str(place_postal_code) 
            print(word) 
            cur = mysql_connect()
            err = insert_place_login_info(cur, username, password, place_name, place_owner_full_name, place_address, place_postal_code,word)
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


@app.route('/change', methods=['POST', 'GET']) 
def change():  
    cur = mysql_connect()
    if request.method == 'POST':  
        value = False
        vist_search = request.form["search"]
        sql = f"SELECT user_id,first_name,last_name,email,phonenumber,address,infected from visitor WHERE first_name='{vist_search}';"  
        cur.execute(sql)  
        data = cur.fetchall()  
        if data is None: 
            value = True  
            return render_template("hospital_portal.html", value=value) 

        return render_template("hospital_portal.html", data=data)  
    else: 
        return render_template("hospital_portal.html")
@app.route('/append', methods=['POST', 'GET']) 
def append():     
    cursor = mysql_connect() 
    if request.method == "POST":  
        vist_id = request.form["id"] 
        vist_inf = request.form["Infected"]  #infected 0 being false and 1 being true
        stat = f"SELECT * from visitor WHERE user_id='{vist_id}';" #updating the infected the value 
        cursor.execute(stat) 
        value = cursor.fetchone()
        if (int(vist_inf) == 1 or int(vist_inf) == 0) and value != None:  #checking for valif id and infected value
            cursor.execute("UPDATE visitor SET infected = %s WHERE user_id = %s", 
               (vist_inf,vist_id,))
            mysql.connection.commit()
            return render_template("hospital_portal.html") 
        else:  
            return "Infected should be between 0 and 1 or wrong id"
    else: 
        return render_template("hospital_portal.html")

@app.route('/agentaddhospital', methods=['POST', 'GET'])
def agentaddhospital(): 
    try: 
        if session['is_logged_in'] and session['user_type'] == "agent":
            if request.method == "POST": 
                commit_flag = True
                age_flag = False
                confirm_password_flag = False
                dup_user_flag = False  
                dup_user_id = False
                success_registration_flag = False
                internal_server_error_flag = False
                vist_name = request.form["username"] 
                vist_password = request.form["password"] 
                vist_pass_cnf = request.form["confirm_password"] 
                vist_hosp_name = request.form["hosp_name"] 
                vist_hosp_id = request.form["hosp_id"]  
                if vist_password != vist_pass_cnf:
                    commit_flag = False
                    confirm_password_flag = True 
                if commit_flag: 
                    cur = mysql_connect()   
                    err = insert_agent_hospital(cur,vist_name,vist_password,vist_hosp_name,vist_hosp_id)
                    if err != 0: 
                        if err == 1062:
                            dup_user_flag = True 
                        if err == 1063: 
                            dup_user_id = True
                        elif err == -1: 
                            internal_server_error_flag = True
                    cur.close() 
                if not internal_server_error_flag and not dup_user_flag and not age_flag and not confirm_password_flag:
                        success_registration_flag  = True
                return agent_add_hospital(success_registration=success_registration_flag,
                                    internal_server_error = internal_server_error_flag,
                                    dup_user_error = dup_user_flag,
                                    age_error = age_flag, 
                                    dup_id_error = dup_user_id, 
                                    confirm_password_error = confirm_password_flag) 
            else: 
                return agent_add_hospital()
        
    except:
        pass
    

@app.route('/registration_navigation', methods=['POST', 'GET'])
@auto.doc()
def registration_navigation():
    """Registration navigation backend

    Content:
        Navigate between visitor or establishemnt owner registration page
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
    return registration_navigation_page()

@app.route('/docs')
@auto.doc()
def documentation():
    return auto.html(title='Corona Archive API documentation')

if __name__ == '__main__':
    app.run(debug=True)

