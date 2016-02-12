import os


class Config:
    pass


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost:4999'
    PUCKTRACKER_URL = 'http://localhost:8002'


class DevelopmentConfig(Config):
    PUCKTRACKER_URL = os.environ.get('PUCKTRACKER_URL', 'http://localhost:8001')
    DEBUG = True


class ProductionConfig(Config):
    PUCKTRACKER_URL = os.environ.get('PUCKTRACKER_URL',
                                     'http://pucks.synchrotron.org.au')


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
