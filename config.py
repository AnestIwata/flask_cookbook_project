import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'biggest-secret-ever'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')