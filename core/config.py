import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    ENV: str = os.getenv('ENV', 'development')
    DEBUG: bool = os.getenv('DEBUG', True)
    APP_HOST: str = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT: str = os.getenv('APP_PORT', 8000)
    DB_USER: str = os.getenv('DB_USER', 'gymlog')
    DB_PASS: str = os.getenv('DB_PASS', 'gymlog')
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_NAME: str = os.getenv('DB_NAME', 'gymlog')
    DB_URL: str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'gymlog')
    JWT_ALGORITHM = 'HS256'
    SENTRY_SDN: str = os.getenv('SENTRY_DSN')


@dataclass(frozen=True)
class DevelopmentConfig(Config):
    DEBUG = True


@dataclass(frozen=True)
class TestingConfig(Config):
    DEBUG = True


@dataclass(frozen=True)
class ProductionConfig(Config):
    DEBUG = False


def get_config():
    env = os.getenv('ENV', 'development')
    config_type = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    return config_type[env]
