import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    POSTS_PER_PAGE = 12


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
