from flask import Flask
from .config import get_config
from .extensions import db, migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    # JWT cookie settings…
    app.config.setdefault("JWT_TOKEN_LOCATION", ["cookies"])
    app.config.setdefault("JWT_COOKIE_SECURE", False)
    app.config.setdefault("JWT_COOKIE_SAMESITE", "Lax")
    app.config.setdefault("JWT_COOKIE_CSRF_PROTECT", False)
    app.config.setdefault("JWT_SECRET_KEY", app.config.get("SECRET_KEY"))

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS (safe even if same-origin)
    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://questboard-env.eba-3rfff74z.eu-north-1.elasticbeanstalk.com"
    ]}}, supports_credentials=True)

    # Blueprints
    from .routes import bp as core_bp
    app.register_blueprint(core_bp)

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .pages import pages           # ← add
    app.register_blueprint(pages)      # ← add

    return app
