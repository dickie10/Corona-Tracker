# SE-Sprint01-Team23

# README for Corona Archive

### Contributors

Sprint 1
- Shishir Sunar
- Jona Bako

Sprint 2 
- Suyash Thapa 
- Julian Jermiah Weske 

## About the Project

The Corona Archive project is a web application which aims to control the spreading of the COVID-19 disease. The project includes the tracking of users locations by their respective visiting places. In general, there will be four different types of users using this web application.

1. Visitors: Citizens or visitors will use the web service to indicate whether they have entered a particular place and when they have done so.
2. Places: Places which are frequently visited by people, such as clubs, pubs, restaurants, cinemas etc. will use the web service to get access to a QR code, which uniquely identifies their place. Citizens will scan this QR code to record their presence at that place.
3. Agency: The agency or the evaluation client will use the web service to generate coronarelated reports by collecting data from the database.
4. Hospital: Hospitals will use the web service to mark people as infected and track anyone else that has been in contact with an infected person

### Built with
* HTML
* CSS
* [Python3](https://www.python.org/download/releases/3.0/)
* [Flask](https://www.fullstackpython.com/flask.html)
* [MySQL](https://www.mysql.com/)

## File Structure
```
\--SE-Sprint01-Team23
        \--static
            \--css                  # All the CSS Files used
            \--img                  # All the images used 
        \--templates    
            \--                     # Main HTML files    
        \--sql  
            \--                     # SQL Query used for initialization
        \--tests
            |--test_sprint1.py      # Main Testing Python Code
        -- app.py                    # Main Python Code
        -- README.md
        -- requirements.txt          # Required flask dependencies to run this program
        -- .gitignore    
```

## Getting Started

### Prerequisites

* [Mysql](https://dev.mysql.com/downloads/installer/)
* Flask 
```
pip3 install Flask
```
* Virtual Env:
You must have virtual environment module installed in default (generally).

## Installation Guide

```bash
# Clone the repo.
git clone https://github.com/Magrawal17/SE-Sprint01-Team23.git -> only for sample
cd SE-Sprint01-Team23/

# Create virtual environment
$ python3 -m venv se-env

# Start virtual environment
$ source se-env/bin/activate

# Install all the dependencies
$ pip3 install -r requirements.txt

# Open  MySQL
$ mysql -u {YOUR CURRENT USERNAME OR ROOT} -p

# Run this command in MYSQL command line to create required database.
mysql>create database corona_archive;
mysql>use corona_archive;
mysql> source sql/data.sql
mysql> exit

# Create db.yaml file 
$ touch db.yaml

# Open db.yaml and enter database credentials in the file format described below
$ nano db.yaml

# Run python server
$ python3 app.py

```

### `db.yaml` file Format. Enter your respective credentials

We tried using ClamV so that it would be easier for the user. However clamv did not support the required flask dependices to run this program.

```yaml
mysql_hostname: "localhost"
mysql_username: "{YOUR USERNAME CHANGE THIS WHEN TYPING IN YOUR COMPUTER}"
mysql_password: "{YOUR PASSWORD CHANGE THIS WHEN TYPING IN YOUR COMPUTER}"
mysql_database: "corona_archive"
```

# View Documentation

Go to this URL once the server has started.

```
http://localhost:5000/docs
```
# Run tests

Run this code once you are on the entire environment

```sh
$ python3 tests/test.py
```
# Sprint 2 Changes done 
- Created QR Code scanner for the visitors 
- Added the functionality of generating the qr code to the place
- Added the functionality of downloading the qr code by the place owners
- Added the functionality of searching visitors by hospital
- Hospital now can edit whether a person is infected or not
- Added QRcode column in table 'place'
- Added hospital registration functionality to agent 
- Created 'visitedPlace' Table in the database
- Created a connection between visitor id and user id
- Created a functionality to show the visitor id, arrival time,departure time for agent  
- Created a functionaity of the agent being able to download the visited place data 
- Changed the testcase according to requirements in the site
- Created more testcases for testing the web app
# Added requirements 
- qrcode7.3.1 to use qr code generation 
- Pillow9.1.0 to use display the qr code 

Intially,the website had just basic registrationa and log in functionality. This sprint we added all the required functionality required for the corona archive web app. The project is 90% done only few changes on the front end design is left for the other sprints. A visitor can now scan a qr code and time log can be stored in the database,owners can generate there qr code and download it.Hospitals can view visitors and edit the changes on the infected report of the visitors,Lastly agent can add hospitals to database and agent can also check on the visitors time log with connection with the place id. 
## Acknowledgments

* Special thanks to Mr. Mahiem Agrawal for guiding through the task.
