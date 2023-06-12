import os
import cloudinary
from flask import Flask
from sqlalchemy import MetaData
from config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata, engine_options={"pool_pre_ping": True})
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
mail = Mail()

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
    mail.init_app(app)

    from flaskr.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from flaskr.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from flaskr.auth.paypal import bp as paypal_bp
    app.register_blueprint(paypal_bp)

    from flaskr.admin.base import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from flaskr.user.base import bp as user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    return app


from flaskr.models.person import Person
from flaskr.models.student import Student
from flaskr.models.course import Course
from flaskr.models.change import Change
from flaskr.models.student_course import student_course
from flaskr.models.purchase_paypal import PurchasePaypal
from flaskr.models.cycle import Cycle
from flaskr.models.video import Video
from flaskr.models.material import Material
