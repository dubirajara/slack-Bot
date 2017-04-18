# coding: utf-8

from app import app
import unittest


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.index = self.client.get('/')
        self.api = self.client.post('/api/slackbot')
        self.api_get = self.client.get('/api/slackbot')

    def test_get_index(self):
        self.assertEqual(self.index.status_code, 200)

    def test_post_api(self):
        self.assertEqual(self.api.status_code, 200)

    def test_get_api(self):
        self.assertEqual(self.api_get.status_code, 405)

    def test_content_type_index(self):
        self.assertIn('text/html', self.index.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
