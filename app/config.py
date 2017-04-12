import os


class Config(object):
    SLACK_WEBHOOK_SECRET = 'YOUR SLACK TOKEN WEBHOOK'
    SLACK_TOKEN = ('YOUR SLACK TOKEN USER BOT', None)


class DevConfig(Config):
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
