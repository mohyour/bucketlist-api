import os


class BaseConfig(object):
    """Base Configuration"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    """Test Configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_bucket_db'
    DEBUG = True


class StagingConfig(BaseConfig):
    """Staging Configuration"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False
    TESTING = False

# Dictionary to hold and export all configuraion class
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
