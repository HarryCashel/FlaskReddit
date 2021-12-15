import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # dev mode jwt key, doesn't matter not private
    JWT_SECRET_KEY = "duck"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.getenv("DB_URI")

        if not value:
            raise ValueError("DB_URI is not set")

        return value

    @property
    def SECRET_KEY(self):
        key = os.getenv("SECRET_KEY")

        if not key:
            raise ValueError("SECRET_KEY is not set")

        return key


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):

    @property
    def JWT_SECRET_KEY(self):
        value = os.getenv("JWT_SECRET_KEY")

        if not value:
            raise ValueError("JWT_SECRET_KEY is not set")
        return value


class TestingConfig(Config):
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.getenv("DB_TEST_URI")

        if not value:
            raise ValueError("DB_TEST_URI is not set")

        return value

    @property
    def SECRET_KEY(self):
        key = os.getenv("SECRET_KEY")

        if not key:
            raise ValueError("SECRET_KEY is not set")

        return key


environment = os.getenv("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
