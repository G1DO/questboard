import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{INSTANCE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False

def get_config(name: str | None):
    name = name or os.getenv("FLASK_ENV", "development")
    return DevConfig if name.startswith("dev") else ProdConfig
