from flask import Flask
from .config import get_config




def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))


    # Blueprints
    from .routes import bp as core_bp
    app.register_blueprint(core_bp)


    return app