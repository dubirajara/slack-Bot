# coding: utf-8
import json
from app import app
from models import db, Slack
import unittest


class FlaskAppTestCase(unittest.TestCase):


    def setUp(self):
        self.client = app.test_client()
        db.create_all()
        self.content = Slack(
            username='testuser',
            content='hello word, this is a test',
            channel='SlackTest',
            channel_id='TEST123',
            timestamp=122344557
        )
        db.session.add(self.content)
        db.session.commit()
        self.index = self.client.get('/')
        self.api = self.client.post('/api/slackbot')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_user(self):
        self.assertEqual(self.content.username, 'testuser')

    def test_get_index(self):
        self.assertEqual(self.index.status_code, 200)

    def test_post_api(self):
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


if __name__ == '__main__':
    unittest.main()
