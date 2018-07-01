import unittest
import sys
sys.path.append("..")
from src import create_app, db


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client.post('/auth/signup', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client.post('/auth/signin', data=user_data)

    def create_bucketlist(self, bucketlist, token):
        return self.client.post('/lists',
                                headers=dict(Authorization="Bearer " + token),
                                data=bucketlist)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
