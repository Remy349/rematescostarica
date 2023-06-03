import os
import cloudinary
from flask import Flask
from config import DevelopmentConfig, ProductionConfig, ProductionTestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

db = SQLAlchemy(engine_options={"pool_pre_ping": True})
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()

login_manager.login_view = "auth.ingresar"
login_manager.login_message = "Inicia sesión antes de acceder!"
login_manager.login_message_category = "error"


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    from flaskr.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from flaskr.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from flaskr.admin.base import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app


from flaskr.models.person import Person
from flaskr.models.student import Student
from flaskr.models.course import Course
from flaskr.models.change import Change
