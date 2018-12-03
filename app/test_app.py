import unittest

from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.index = self.client.get('/')

    def test_get_index(self):
        self.assertEqual(self.index.status_code, 200)

    def test_post_api(self):
        self.api = self.client.post('/api/slackbot')
        self.assertEqual(self.api.status_code, 200)

    def test_index_context(self):
        self.assertIn(b'python <b>madrid</b> learn</h3>', self.index.data)

    def test_get_api(self):
        api_get = self.client.get('/api/slackbot')
        self.assertEqual(api_get.status_code, 405)

    def test_get_not_found(self):
        resp = self.client.get("/not-found")
        self.assertEqual(resp.status_code, 404)

    def test_content_type_index(self):
        self.assertIn('text/html', self.index.headers['Content-Type'])

    def test_get_api_list(self):
        api_get = self.client.get('/api/list/')
        self.assertEqual(api_get.status_code, 200)

    def test_get_api_list_id(self):
        api_get = self.client.get('/api/list/200/')
        self.assertEqual(api_get.status_code, 200)


if __name__ == '__main__':
    unittest.main()
