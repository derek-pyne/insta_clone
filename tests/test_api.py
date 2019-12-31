import json
import unittest
from base64 import b64encode

from app import create_app, db
from app.models import User


class APITestCase(unittest.TestCase):
    sample_post_request = {
        'instagram_post_hash': '123',
        'influencer':          'cool_influencer',
        'img_file':            'pic.png',
        'influencer_caption':  'I am cool',
        'alt_text':            'Picture of rock star',
    }
    sample_managed_instagram_account_request = {
        'handle': 'epic_rock_star',
    }

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept':        'application/json',
            'Content-Type':  'application/json'
        }

    def insert_example_user(self):
        u = User(email='john@example.com', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

    def example_user_auth_headers(self):
        return self.get_api_headers("john@example.com", 'cat')

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password')
        )
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_no_auth(self):
        response = self.client.get('/api/v1/posts/',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_bad_auth(self):
        self.insert_example_user()

        # authenticate with bad password
        response = self.client.get(
            '/api/v1/posts/',
            headers=self.get_api_headers('john@example.com', 'dog'))
        self.assertEqual(response.status_code, 401)

    def test_token_auth(self):
        self.insert_example_user()

        # issue a request with a bad token
        response = self.client.get(
            '/api/v1/posts/',
            headers=self.get_api_headers('bad-token', ''))
        self.assertEqual(response.status_code, 401)

        # get a token
        response = self.client.post(
            '/api/v1/tokens/',
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the token
        response = self.client.get(
            '/api/v1/posts/',
            headers=self.get_api_headers(token, ''))
        self.assertEqual(response.status_code, 200)

    def test_unconfirmed_account(self):
        # add an unconfirmed user
        u = User(email='john@example.com', password='cat', confirmed=False)
        db.session.add(u)
        db.session.commit()

        # get list of posts with the unconfirmed account
        response = self.client.get(
            '/api/v1/posts/',
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 403)

    def test_create_edit_and_get_post(self):
        self.insert_example_user()

        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_post_request))
        self.assertEqual(post_response.status_code, 201)
        self.assertDictEqual(
            {k: v for k, v in post_response.json.items() if k not in ['id', 'caption', 'created_at', 'updated_at']},
            {k: v for k, v in self.sample_post_request.items() if
             k not in ['id', 'caption', 'created_at', 'updated_at']}
        )

        get_response = self.client.get(
            '/api/v1/posts/' + str(post_response.json['id']),
            headers=self.example_user_auth_headers())
        self.assertEqual(get_response.status_code, 200)
        saved_post = get_response.json
        self.assertEqual(get_response.json, post_response.json)

        patch_change = {
            'caption': 'Epic new caption'
        }
        patch_response = self.client.patch(
            '/api/v1/posts/' + str(post_response.json['id']),
            headers=self.example_user_auth_headers(),
            data=json.dumps(patch_change))
        self.assertEqual(patch_response.status_code, 200)
        saved_post.update(patch_change)
        self.assertEqual(patch_response.json, saved_post)

    def test_create_post_with_id_should_400(self):
        self.insert_example_user()
        post = {
            'id':                 '123',
            'influencer':         'cool_influencer',
            'img_file':           'pic.png',
            'influencer_caption': 'I am cool',
            'alt_text':           'Picture of rock star',
        }
        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(post))
        self.assertEqual(post_response.status_code, 400)

    def test_create_post_with_existing_should_400(self):
        self.insert_example_user()

        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_post_request))
        self.assertEqual(post_response.status_code, 201)

        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_post_request))
        self.assertEqual(post_response.status_code, 400)

    def test_get_posts(self):
        self.insert_example_user()

        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_post_request))
        self.assertEqual(post_response.status_code, 201)

        second_post = self.sample_post_request.copy()
        second_post['instagram_post_hash'] = '456'
        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(second_post))
        self.assertEqual(post_response.status_code, 201)

        get_response = self.client.get(
            '/api/v1/posts/',
            headers=self.example_user_auth_headers())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json['posts']), 2)

    def test_create_edit_and_get_managed_instagram_account(self):
        self.insert_example_user()

        post_response = self.client.post(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_managed_instagram_account_request))
        self.assertEqual(post_response.status_code, 201)
        self.assertDictEqual(
            {k: v for k, v in post_response.json.items() if k not in ['id', 'created_at', 'updated_at', 'posts']},
            {k: v for k, v in self.sample_managed_instagram_account_request.items() if
             k not in ['id', 'created_at', 'updated_at']}
        )

        get_response = self.client.get(
            '/api/v1/managed_instagram_accounts/' + str(post_response.json['id']),
            headers=self.example_user_auth_headers())
        self.assertEqual(get_response.status_code, 200)
        saved_managed_instagram_account = get_response.json
        self.assertEqual(get_response.json, post_response.json)

        patch_change = {
            'handle': 'epic-new-handle'
        }
        patch_response = self.client.patch(
            '/api/v1/managed_instagram_accounts/' + str(post_response.json['id']),
            headers=self.example_user_auth_headers(),
            data=json.dumps(patch_change))
        self.assertEqual(patch_response.status_code, 200)
        saved_managed_instagram_account.update(patch_change)
        self.assertEqual(patch_response.json, saved_managed_instagram_account)

    def test_create_managed_instagram_account_with_id_should_400(self):
        self.insert_example_user()
        managed_instagram_account = {
            'id':     '123',
            'handle': 'cool_influencer',
        }
        post_response = self.client.post(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(managed_instagram_account))
        self.assertEqual(post_response.status_code, 400)

    def test_create_managed_instagram_account_with_existing_should_400(self):
        self.insert_example_user()

        post_response = self.client.post(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_managed_instagram_account_request))
        self.assertEqual(post_response.status_code, 201)

        post_response = self.client.post(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_managed_instagram_account_request))
        self.assertEqual(post_response.status_code, 400)

    def test_get_managed_instagram_accounts(self):
        self.insert_example_user()

        post_response = self.client.post(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(self.sample_managed_instagram_account_request))
        self.assertEqual(post_response.status_code, 201)

        second_post = self.sample_managed_instagram_account_request.copy()
        second_post['handle'] = 'new_rock_star'
        post_response = self.client.post(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers(),
            data=json.dumps(second_post))
        self.assertEqual(post_response.status_code, 201)

        get_response = self.client.get(
            '/api/v1/managed_instagram_accounts/',
            headers=self.example_user_auth_headers())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json['managed_instagram_accounts']), 2)
