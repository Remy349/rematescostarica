import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=2)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + os.path.join(basedir, "remates.db")


class ProductionTestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("REMATES_DB_URL_TEST")


class ProductionConfig(Config):
    pass
