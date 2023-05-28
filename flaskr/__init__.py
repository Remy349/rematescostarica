from flask import Flask
from config import DevelopmentConfig, ProductionConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    from flaskr.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from flaskr.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
