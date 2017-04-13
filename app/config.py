import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
