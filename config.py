class Config(object):
    """Base configuration
    configurations settings that apply to all the environments.
    """

    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""

    ENV = "production"


class DevelopmentConfig(Config):
    """Development configuration"""

    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
