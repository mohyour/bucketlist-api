import unittest
import json
from src import db, create_app


class TestUserAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user = {
            "username": "moyosore",
            "email": "moyosore@gmail.com",
            "password": "my_password"
        }
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_signup(self):
        user = self.client.post('/auth/signup', data=self.user)
        data = json.loads(user.data.decode())
        self.assertEqual(user.status_code, 201)
        self.assertEqual(data['message'], "You registered successfully.")

    def test_user_already_exist(self):
        user = self.client.post('/auth/signup', data=self.user)
        data = json.loads(user.data.decode())
        same_user = self.client.post('/auth/signup', data=self.user)
        same_user_data = json.loads(same_user.data.decode())
        self.assertEqual(same_user.status_code, 409)
        self.assertEqual(same_user_data['message'], "User already exist.")

    def test_user_signin(self):
        user = self.client.post('/auth/signup', data=self.user)
        self.assertEqual(user.status_code, 201)
        login_user = self.client.post('/auth/signin', data=self.user)
        response = json.loads(login_user.data.decode())
        self.assertEqual(login_user.status_code, 201)
        self.assertEqual(response['message'], "You are now logged in")
        self.assertTrue(response['token'])

    def test_not_registered_user(self):
        user = self.client.post('/auth/signin', data=self.user)
        self.assertEqual(user.status_code, 401)
        response = json.loads(user.data.decode())
        self.assertEqual(response["message"], "Incorrect login details")
