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
        bucket = self.client.post('/lists/', data=self.bucketlist)
        self.assertEqual(bucket.status_code, 201)
        response = self.client.get('/lists/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Travel the world', data[0]["name"])


    def test_get_bucketlist_by_id(self):
        """Get bucket by id"""
        bucket = self.client.post('/lists/', data=self.bucketlist)
        data = json.loads(bucket.data.decode())
        response = self.client.get('/lists/{}'.format(data["id"]))
        data = json.loads(response.data.decode())
        self.assertEqual(data["id"], 1)


    def test_edit_bucketlist(self):
        bucket = self.client.post('/lists/', data=self.bucketlist)
        bucket_data = json.loads(bucket.data.decode())
        response = self.client.put("/lists/{}".format(bucket_data["id"]),
        data={"name": "New edit - travel round the world"})
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 200)
        self.assertEqual(bucket_data["id"], data["id"])
        self.assertEqual(data["name"], "New edit - travel round the world")


    def test_delete_bucketlist(self):
        bucket = self.client.post('/lists/', data=self.bucketlist)
        bucket_data = json.loads(bucket.data.decode())
        response = self.client.delete('/lists/{}'.format(bucket_data["id"]))
        data = json.loads(response.data.decode())
        result = self.client.get('/lists/{}'.format(bucket_data["id"]))
        self.assertEqual(result.status_code, 404)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Bucket list successfully deleted")
        self.assertEqual(result.status_code, 404)


    def tearDown(self):
        """teardown all initialized variables."""

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
