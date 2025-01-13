import os

class BaseConfig:
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    FLASK_ENV: str = os.environ.get("FLASK_ENV", "development")

class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL") or "sqlite:///dev.db"

class TestingConfig(BaseConfig):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL") or "postgresql://localhost/production_db"

def get_config():
    env = os.environ.get("FLASK_ENV", "development").lower()
    if env == "development":
        return DevelopmentConfig
    elif env == "testing":
        return TestingConfig
    elif env == "production":
        return ProductionConfig
    else:
        raise ValueError(f"Unknown FLASK_ENV value: {env}")