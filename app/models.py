from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Slack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    content = db.Column(db.String(500), index=True)
    channel = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.String(100), index=True)

    def __init__(self, username, content, channel, timestamp):
        self.username = username
        self.content = content
        self.channel = channel
        self.timestamp = timestamp

    def __repr__(self):
        return '<User %r>' % (self.username)
