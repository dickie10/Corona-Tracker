import os, sys
import string
import random
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import tempfile
import unittest

from app import app
from flask_mysqldb import MySQL



class FlaskTestCase(unittest.TestCase):
    #Some test cases depends upon the data stored in the database

    # Working Test Cases - 19

    #The index page test case
    def test_index_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type="html/text")
        self.assertIn(b'Corona Archive', response.data)

    # The login page test case
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type="html/text")
        self.assertIn(b'Log In', response.data)

    #The visitor registration page
    def test_visitor_registration_page(self):
        tester = app.test_client(self)
        response = tester.get('/visitor_registration', content_type="html/text")
        self.assertIn(b'Visitor registration', response.data)
    #The establishment owner registration page
    def test_place_registration_page(self):
        tester = app.test_client(self)
        response = tester.get('/place_registration', content_type="html/text")
        self.assertIn(b'Establishment registration', response.data)
    
    #Test for successful login. Here please change the username and password by the avaliable data in the database.
    def test_visitor_login_success(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="qq", password="qq", user_type = "visitor"), follow_redirects=True)
        self.assertIn(b'Welcome visitor', response.data)

    #Test for logout page
    def test_logout_page(self):
        tester = app.test_client(self)
        response = tester.get('/logout', content_type="html/text")
        self.assertIn(b'You have successfully logged out', response.data)

    #Test for duplicate username for visitor
    def test_duplicate_visitor_registration(self):
        tester = app.test_client(self)
        response = tester.post('/visitor_registration', data=dict(username="qq", 
                    password="qq", 
                    confirm_password = "qq",
                    first_name = "qq",
                    last_name = "qq",
                    age = "12",
                    gender = "male"), follow_redirects=True)
        self.assertIn(b'Username already exists', response.data)
    
    #Test for confirm password mismatch visitor
    def test_password_mismatch_visitor_registration(self):
        tester = app.test_client(self)
        response = tester.post('/visitor_registration', data=dict(username="mm", 
                    password="qq", 
                    confirm_password = "qqq",
                    first_name = "qq",
                    last_name = "qq",
                    age = "12",
                    gender = "male"), follow_redirects=True)
        self.assertIn(b'Password donot match', response.data)

    #Test for duplicate username for establishment owner
    def test_duplicate_place_registration(self):
        tester = app.test_client(self)
        response = tester.post('/place_registration', data=dict(username="q", 
                    password="q", 
                    confirm_password = "q",
                    place_name = "q",
                    place_owner_full_name = "q",
                    place_postal_code = "12",
                    place_address = "xyz"), follow_redirects=True)
        self.assertIn(b'Username already exists', response.data)
    
    #Test for confirm password mismatch establishment owner
    def test_password_mismatch_place_registration(self):
        tester = app.test_client(self)
        response = tester.post('/place_registration', data=dict(username="mm", 
                    password="q", 
                    confirm_password = "qsdfs",
                    place_name = "q",
                    place_owner_full_name = "q",
                    place_postal_code = "12",
                    place_address = "xyz"), follow_redirects=True)
        self.assertIn(b'Password donot match', response.data)

    #Test for visitor login redirection incase of portaling in without session
    def test_login_redirection_visitor_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/visitor_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data)
    
    #Test for establishment owner login redirection incase of portaling in without session
    def test_login_redirection_place_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/place_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data)
    
    #Test for agent login redirection incase of portaling in without session
    def test_login_redirection_agent_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/agent_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data)
    
    #Test for hospital login redirection incase of portaling in without session
    def test_login_redirection_hospital_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/hospital_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data)
    
    #Test for visitor login
    def test_visitor_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="qq", 
                    password="qq", 
                    user_type = "visitor"), follow_redirects=True)
        self.assertIn(b'Welcome visitor', response.data)
    
    #Test for establishment owner login
    def test_place_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="q", 
                    password="q", 
                    user_type = "place"), follow_redirects=True)
        self.assertIn(b'Welcome establishment owner', response.data)

    #Test for agent login
    def test_agent_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="q", 
                    password="q", 
                    user_type = "agent"), follow_redirects=True)
        self.assertIn(b'Welcome agent', response.data)

    #Test for hospital login
    def test_hospital_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="q", 
                    password="q", 
                    user_type = "hospital"), follow_redirects=True)
        self.assertIn(b'Welcome hospital', response.data)
    
    #Test for navigation page
    def test_registration_navigation(self):
        tester = app.test_client(self)
        response = tester.get('/registration_navigation', content_type="html/text")
        self.assertIn(b'Registration navigation', response.data)
    
if __name__=='__main__':
   unittest.main()