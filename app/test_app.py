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

    def test_get_invite(self):
        self.assertEqual(self.api.status_code, 200)

    def test_content_type(self):
        self.assertIn('text/html', self.index.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
