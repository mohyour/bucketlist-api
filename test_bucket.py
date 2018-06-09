import os
import json
import unittest
from src import create_app, db, app

class TestBucketList(unittest.TestCase):
    def setUp(self):
        # self.app = create_app(config_name="testing")
        self.client = app.test_client
        self.bucketlist = {"name": "Get to D2"}

        # bind app to current context
        with app.app_context():
            db.create_all()

    def test_create_bucket_list(self):
        """Test api create list"""
        response = self.client().post("/lists/", data=self.bucketlist)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Get to D2")


    def test_get_all_bucket_lists(self):
        """Test API can get a bucketlist (GET request)."""
        response = self.client().post('/lists/', data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/lists/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        print(data, "data")
        self.assertEqual('Get to D2', data[0]["name"])

    def tearDown(self):
        """teardown all initialized variables."""
        with app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
            # del self.app
        # del self._ctx
