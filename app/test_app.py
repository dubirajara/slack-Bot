# coding: utf-8

from app import app
import unittest


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.index = self.client.get('/')
        self.api = self.client.post('/api/slackbot')

    def test_get_index(self):
        self.assertEqual(self.index.status_code, 200)

    def test_post_api(self):
        self.assertEqual(self.api.status_code, 200)

    def test_get_api(self):
        api_get = self.client.get('/api/slackbot')
        self.assertEqual(api_get.status_code, 405)

    def test_get_not_found(self):
        resp = self.client.get("/not-found")
        self.assertEqual(resp.status_code, 404)

    def test_content_type_index(self):
        self.assertIn('text/html', self.index.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
