import unittest
import os
import json
from base import BaseTest


class BucketlistTestCase(BaseTest):
    """Bucketlist test case"""
    bucketlist = {'name': 'Travel to Hawai for vacation'}

    def test_bucketlist_creation(self):
        """Can create a bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Travel to Hawai for vacation', str(res.data))

    def test_user_cannot_create_with_incorrect_auth(self):
        self.register_user()
        self.login_user()
        res = self.create_bucketlist(self.bucketlist, 'incorrect token')
        self.assertIn("Please provide a valid token", str(res.data))

    def test_user_cannot_get_unavailable_bucketlist(self):
        """Cannot get unavailable bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        result = self.client.get(
            '/lists/200',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)
        self.assertIn('Bucket list not found', str(result.data))

    def test_user_cannot_edit_unavailable_bucketlist(self):
        """Cannot edit unavailable bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        result = self.client.put(
            '/lists/200',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(result.status_code, 404)
        self.assertIn('Bucket list not found', str(result.data))

    def test_user_cannot_delete_unavailable_bucketlist(self):
        """Cannot edit unavailable bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        result = self.client.delete(
            '/lists/200',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(result.status_code, 404)
        self.assertIn('Bucket list not found', str(result.data))

    def test_api_can_get_all_bucketlists(self):
        """Can get a bucketlist"""
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
        """Can get a single bucketlist by using it's id."""
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
        """Can edit an existing bucketlist"""
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
        """Can delete an existing bucketlist."""
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

    def test_cannot_edit_delete_another_user_buck(self):
        """Cannot delete or edit annother user's bucketlist."""
        self.register_user()
        user1 = self.login_user()
        access_token = json.loads(user1.data.decode())['token']
        user1_list = self.create_bucketlist(self.bucketlist, access_token)
        self.assertEqual(user1_list.status_code, 201)
        user1_data = json.loads(user1_list.data.decode())

        self.register_user('user2@user.com', 'pass')
        user2 = self.login_user('user2@user.com', 'pass')
        user2_access_token = json.loads(user2.data.decode())['token']
        user2_list = self.create_bucketlist(
            self.bucketlist, user2_access_token)
        user2_data = json.loads(user2_list.data.decode())

        delete_list = self.client.delete(
            '/lists/{}'.format(user1_data['id']),
            headers=dict(Authorization="Bearer " + user2_access_token))
        self.assertEqual(delete_list.status_code, 401)
        self.assertIn(
            "You cannot delete another user\\\'s bucketlist", str(delete_list.data))

        edit_list = self.client.put(
            '/lists/{}'.format(user2_data['id']),
            data=self.bucketlist,
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(edit_list.status_code, 401)
        self.assertIn(
            "You cannot edit another user\\\'s bucketlist", str(edit_list.data))


if __name__ == "__main__":
    unittest.main()
