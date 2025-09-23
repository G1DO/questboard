from flask import Flask
from .config import get_config
from .extensions import db, migrate




def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)


    

    # Blueprints
    from .routes import bp as core_bp
    app.register_blueprint(core_bp)

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")


    return app