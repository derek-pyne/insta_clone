import json
import unittest

from app import create_app, db


class APITestCase(unittest.TestCase):
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

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_create_edit_and_get_post(self):
        post = {
            'instagram_post_hash': '123',
            'influencer': 'cool_influencer',
            'img_file': 'pic.png',
            'influencer_caption': 'I am cool',
            'alt_text': 'Picture of rock star',
        }
        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.get_api_headers(),
            data=json.dumps(post))
        self.assertEqual(post_response.status_code, 201)
        self.assertDictEqual(
            {k: v for k, v in post_response.json.items() if k not in ['id', 'caption']},
            {k: v for k, v in post.items() if k not in ['id', 'caption']}
        )

        get_response = self.client.get(
            '/api/v1/posts/' + str(post_response.json['id']),
            headers=self.get_api_headers())
        self.assertEqual(get_response.status_code, 200)
        saved_post = get_response.json
        self.assertEqual(get_response.json, post_response.json)

        patch_change = {
            'caption': 'Epic new caption'
        }
        patch_response = self.client.patch(
            '/api/v1/posts/' + str(post_response.json['id']),
            headers=self.get_api_headers(),
            data=json.dumps(patch_change))
        self.assertEqual(patch_response.status_code, 200)
        saved_post.update(patch_change)
        self.assertEqual(patch_response.json, saved_post)

    def test_create_post_with_id_should_400(self):
        post = {
            'id': '123',
            'influencer': 'cool_influencer',
            'img_file': 'pic.png',
            'influencer_caption': 'I am cool',
            'alt_text': 'Picture of rock star',
        }
        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.get_api_headers(),
            data=json.dumps(post))
        self.assertEqual(post_response.status_code, 400)

    def test_create_post_with_existing_post_should_400(self):
        post = {
            'instagram_post_hash': '123',
            'influencer': 'cool_influencer',
            'img_file': 'pic.png',
            'influencer_caption': 'I am cool',
            'alt_text': 'Picture of rock star',
        }
        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.get_api_headers(),
            data=json.dumps(post))
        self.assertEqual(post_response.status_code, 201)

        post = {
            'instagram_post_hash': '123',
            'influencer': 'cool_influencer',
            'img_file': 'pic.png',
            'influencer_caption': 'I am cool',
            'alt_text': 'Picture of rock star',
        }
        post_response = self.client.post(
            '/api/v1/posts/',
            headers=self.get_api_headers(),
            data=json.dumps(post))
        self.assertEqual(post_response.status_code, 400)