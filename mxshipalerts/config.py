import os


class Config:
    pass


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost:4999'
    PUCKTRACKER_URL = 'http://pucktracker-test'


class DevelopmentConfig(Config):
    PUCKTRACKER_URL = os.environ.get('PUCKTRACKER_DEV_URL', 'http://localhost:8001')
    DEBUG = True


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
}
