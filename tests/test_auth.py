import unittest
import json
from base import BaseTest


class TestUserAuthentication(BaseTest):
    """Users authentication test case"""

    def test_user_signup(self):
        """Test user can signup"""
        user = self.register_user()
        data = json.loads(user.data.decode())
        self.assertEqual(user.status_code, 201)
        self.assertEqual(data['message'], "You registered successfully.")

    def test_user_already_exist(self):
        """Test already existing cannot create create acount"""
        self.register_user()
        same_user = self.register_user()
        same_user_data = json.loads(same_user.data.decode())
        self.assertEqual(same_user.status_code, 409)
        self.assertEqual(same_user_data['message'], "User already exist.")

    def test_user_cannot_signup_invalid_email(self):
        """Test user cannot signup with invalid email"""
        invalid_email = self.register_user("me@me", 'password')
        data = json.loads(invalid_email.data.decode())
        self.assertEqual(invalid_email.status_code, 401)
        self.assertEqual(data['message'], "Invalid email")

    def test_user_cannot_signup_empty_password(self):
        """Test user cannot signup with empty password"""
        empty_password = self.register_user('test@tester.com', '  ')
        data = json.loads(empty_password.data.decode())
        self.assertEqual(data['message'], 'Password cannot be empty.')

    def test_user_cannot_signup_signin_with_no_field(self):
        """Test user cannot signup/signin without specifying meeded fields"""
        no_key_signup = self.client.post('/auth/signup', data='')
        no_key_signin = self.client.post('/auth/signin', data='')
        signin_data = json.loads(no_key_signin.data.decode())
        signup_data = json.loads(no_key_signup.data.decode())
        self.assertEqual(
            signin_data['message'], 'Check payload. email and password are needed')
        self.assertEqual(
            signup_data['message'], 'Check payload. email and password are needed')

    def test_user_signin(self):
        """Test user can signin"""
        user = self.register_user()
        self.assertEqual(user.status_code, 201)
        login_user = self.login_user()
        response = json.loads(login_user.data.decode())
        self.assertEqual(login_user.status_code, 201)
        self.assertEqual(response['message'], "You are now logged in")
        self.assertTrue(response['token'])

    def test_not_registered_user(self):
        """Test users not registered cannoyt signin"""
        user = self.login_user()
        self.assertEqual(user.status_code, 401)
        response = json.loads(user.data.decode())
        self.assertEqual(response["message"], "Incorrect login details")


if __name__ == "__main__":
    unittest.main()
