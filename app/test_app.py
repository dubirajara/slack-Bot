# coding: utf-8

from app import app
import unittest


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.index = self.client.get('/')
        self.api = self.client.post('/api/slackbot')

    def test_get_index(self):
        '''Get home must return HTTP status code 200'''
        self.assertEqual(self.index.status_code, 200)

    def test_post_api(self):
        '''Post endpoint bot must return HTTP status code 200'''
        self.assertEqual(self.api.status_code, 200)

    def test_get_api(self):
        '''Get endpoint bot must return status code 405 Method not allowed'''
        api_get = self.client.get('/api/slackbot')
        self.assertEqual(api_get.status_code, 405)

    def test_get_not_found(self):
        '''Get a page that not exist must return status code 404'''
        resp = self.client.get("/not-found")
        self.assertEqual(resp.status_code, 404)

    def test_content_type_index(self):
        '''html index content type must be HTTP text/html'''
        self.assertIn('text/html', self.index.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
