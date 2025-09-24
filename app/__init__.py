from flask import Flask
from .config import get_config
from .extensions import db, migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()



def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

        # JWT cookie settings (dev-safe defaults)
    app.config.setdefault("JWT_TOKEN_LOCATION", ["cookies"]) # HttpOnly cookies
    app.config.setdefault("JWT_COOKIE_SECURE", False) # True in prod (HTTPS)
    app.config.setdefault("JWT_COOKIE_SAMESITE", "Lax")
    app.config.setdefault("JWT_COOKIE_CSRF_PROTECT", False) # Enable later in prod
    app.config.setdefault("JWT_SECRET_KEY", app.config.get("SECRET_KEY"))




    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


        # CORS (allow dev frontends; tighten in prod)
    CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000", "http://localhost:5173", "http://localhost:8000"
    ]}}, supports_credentials=True)


    

    # Blueprints
    from .routes import bp as core_bp
    app.register_blueprint(core_bp)

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")


    return app