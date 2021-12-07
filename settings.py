import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.getenv("DB_URI")

        if not value:
            raise ValueError("DB_URI is not set")

        return value


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.getenv("DB_TEST_URI")

        if not value:
            raise ValueError("DB_TEST_URI is not set")

        return value


environment = os.getenv("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
