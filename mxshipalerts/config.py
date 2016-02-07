class Config:
    pass


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost:4999'


config = {
    'testing': TestingConfig,
}
