import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = 'development'
    DEBUG: bool = True
    APP_HOST: str = '0.0.0.0'
    APP_PORT: str = 8000
    DB_USER: str = 'fastapi'
    DB_PASS: str = 'fastapi'
    DB_HOST: str = 'localhost'
    DB_NAME: str = 'fastapi'
    DB_URL: str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}'
    JWT_SECRET_KEY: str = 'fastapi'
    JWT_ALGORITHM: str = 'HS256'
    SENTRY_SDN: str = None


class DevelopmentConfig(Config):
    DEBUG: str = True


class TestingConfig(Config):
    DEBUG: str = True


class ProductionConfig(Config):
    DEBUG: str = False


def get_config():
    env = os.getenv('ENV', 'development')
    config_type = {
        'development': DevelopmentConfig(),
        'testing': TestingConfig(),
        'production': ProductionConfig(),
    }
    return config_type[env]
