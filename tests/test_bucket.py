import unittest
import os
import json
from base import BaseTest


class BucketlistTestCase(BaseTest):
    """This class represents the bucketlist test case"""
    bucketlist = {'name': 'Travel to Hawai for vacation'}

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

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Travel to Hawai for vacation', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(res.status_code, 201)
        res = self.client.get(
            '/lists',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Travel to Hawai for vacation', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        res = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        result = self.client.get(
            '/lists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Travel to Hawai for vacation', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        res = self.client.put(
            '/lists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(res.status_code, 200)

        results = self.client.get(
            '/lists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        res = self.client.delete(
            '/lists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)

        result = self.client.get(
            '/lists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

if __name__ == "__main__":
    unittest.main()
