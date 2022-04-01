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

    # Working Test Cases - 22

    def test_index_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type="html/text")
        self.assertIn(b'Corona Archive', response.data)

    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type="html/text")
        self.assertIn(b'Log In', response.data)

    def test_visitor_registration_page(self):
        tester = app.test_client(self)
        response = tester.get('/visitor_registration', content_type="html/text")
        self.assertIn(b'Register as Visitor', response.data) 
    
    def test_place_registration_page(self):
        tester = app.test_client(self)
        response = tester.get('/place_registration', content_type="html/text")
        self.assertIn(b'Register as Establishment', response.data) 

    def test_visitor_login_success(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="qq", password="qq", user_type = "visitor"), follow_redirects=True)
        self.assertEqual(response.status_code, 200) 

    def test_logout_page(self):
        tester = app.test_client(self)
        response = tester.get('/logout', content_type="html/text")
        self.assertIn(b'You have successfully logged out', response.data) 
    
    def test_duplicate_visitor_registration(self):
        tester = app.test_client(self)
        response = tester.post('/visitor_registration', data=dict(username="qq", 
                    password="qq", 
                    confirm_password = "qq",
                    first_name = "qq",
                    last_name = "qq",
                    age = "12",
                    gender = "male",
                    infected = 0, 
                    address = "Bremen",
                    email = "qq@pp.com",
                    phonenumber ="98345678"), follow_redirects=True) 
        self.assertIn(b'Username already exists', response.data) 

    def test_password_mismatch_visitor_registration(self):
        tester = app.test_client(self)
        response = tester.post('/visitor_registration', data=dict(username="mm", 
                    password="qq", 
                    confirm_password = "qqq",
                    first_name = "qq",
                    last_name = "qq",
                    age = "12",
                    gender = "male",
                     infected = 0, 
                    address = "Bremen",
                    email = "qq@pp.com",
                    phonenumber ="98345678"), follow_redirects=True)
        self.assertIn(b'Password donot match', response.data)   
    
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
    
    def test_login_redirection_visitor_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/visitor_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data) 
    
    def test_login_redirection_place_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/place_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data) 
    
    def test_login_redirection_agent_portal(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.get('/agent_portal', content_type="html/text")
        self.assertIn(b'Log In', response.data) 
    
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
        self.assertEqual(response.status_code, 200)

    def test_agent_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="q", 
                    password="q", 
                    user_type = "agent"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_registration_navigation(self):
        tester = app.test_client(self)
        response = tester.get('/registration_navigation', content_type="html/text")
        self.assertIn(b'Registration navigation', response.data) 
    
    def test_hospital_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="q", 
                    password="q", 
                    user_type = "hospital"), follow_redirects=True)
        self.assertEqual(response.status_code, 200) 
    
    def test_place_login(self):
        tester = app.test_client(self)
        tester.get('/logout', content_type="html/text")
        response = tester.post('/login', data=dict(
                    username="q", 
                    password="q", 
                    user_type = "place"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
   
    def test_hospital_register_page(self): 
        tester = app.test_client(self) 
        response = tester.get('/addhospital', content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_display_data(self): 
        tester = app.test_client(self) 
        response = tester.get('/Display', content_type="html/text") 
        self.assertEqual(response.status_code, 200)  
    
    def test_valid_place(self): 
        tester = app.test_client(self) 
        response = tester.post('/read_qr_code', data=dict(code="mm",follow_redirects=True)) 
        self.assertEqual(response.status_code, 200) 
    
    

    

if __name__=='__main__':
   unittest.main()