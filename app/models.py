import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Slack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    content = db.Column(db.Text, index=True)
    channel = db.Column(db.String(100), index=True)
    channel_id = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.String(100), index=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, content, channel, channel_id, timestamp):
        self.username = username
        self.content = content
        self.channel = channel
        self.channel_id = channel_id
        self.timestamp = timestamp

    def __repr__(self):
        return f'<{self.__class__.__name__}, username: {self.username}>'
