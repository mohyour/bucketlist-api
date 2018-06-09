import os
import json
import unittest
from src import create_app, db, app

class TestBucketList(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.bucketlist = {"name": "Travel the world"}

        # bind app to current context
        with self.app.app_context():
            db.create_all()

    def test_create_bucket_list(self):
        """Test api create list"""
        response = self.client.post("/lists/", data=self.bucketlist)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Travel the world")


    def test_get_all_bucket_lists(self):
        """Test API can get a bucketlist (GET request)."""
        response = self.client.post('/lists/', data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/lists/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Travel the world', data[0]["name"])

    def tearDown(self):
        """teardown all initialized variables."""

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
