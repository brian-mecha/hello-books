import os

class Config(object):
    """
    General Config settings that are shared by all environments
    """
    DEBUG = False
    TESTING = False
    ERROR_404_HELP = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mozart@localhost:5432/books_test_db'


class DevelopmentConfig(Config):
    """
    Config settings for Development
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mozart@localhost:5432/hello_books'


class TestingConfig(Config):
    """
    Config setting for Testing
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mozart@localhost:5432/books_test_db'


class ProductionConfig(Config):
    """
    Config settings for Production
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mozart@localhost:5432/hello_books'


config_app = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}