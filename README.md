# SE-Sprint01-Team23

# README for Corona Archive

### Contributors

Sprint 1
- Shishir Sunar
- Jona Bako


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
* Virtual Env
```
sudo pip3 install virtualenv 
```

## Installation Guide

```bash
# Clone the repo.
git clone https://github.com/Magrawal17/SE-Sprint01-Team23.git -> only for sample
cd SE-Sprint01-Team23/

# Create virtual environment
$ virtualenv se-env

# Start virtual environment
$ source se-env/bin/activate

# Install all the dependencies
$ pip3 install -r requirements.txt

# Open  MySQL
$ mysql -u {YOUR CURRENT USERNAME OR ROOT} -p

# Run this command in MYSQL command line to create required database.
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
mysql_host: "localhost"
mysql_user: "{YOUR USERNAME CHANGE THIS WHEN TYPING IN YOUR COMPUTER}"
mysql_password: "{YOUR PASSWORD CHANGE THIS WHEN TYPING IN YOUR COMPUTER}"
mysql_db: "se_team23"
```

# View Documentation

Go to this URL once the server has started.

```
http://localhost:5000/docs
```
# Run tests

Run this code once you are on the entire environment

```sh
$ python3 tests/test_sprint1.py
```

## Acknowledgments

* Special thanks to Mr. Mahiem Agrawal for guiding through the task.
