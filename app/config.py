import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "ASCII Converter"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    DEBUG = os.getenv("FLASK_DEBUG", True)
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    DATA_DIR = os.getenv("DATA_DIR", "temp")
    OUT_DIR = os.getenv("OUT_DIR", "out")
