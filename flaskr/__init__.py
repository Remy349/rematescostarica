import os
import paypalrestsdk
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from config import Config
from flask_moment import Moment

load_dotenv()

app = Flask(__name__)

PAYPAL_MODE = os.getenv("PAYPAL_MODE")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

paypalrestsdk.configure({
    "mode": PAYPAL_MODE,
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_CLIENT_SECRET,
})

if not Config.SQLALCHEMY_DATABASE_URI:
    raise RuntimeError("DATABASE_URI is not set!")
else:
    print("DATABASE_URI is ok!!!")

app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = "flaskr/static/img"

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

Session(app)

moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    """ Funcion para manejar el error 404 """
    return render_template("errors/404.html"), 404

from flaskr import routes
from flaskr import auth
from flaskr import paypal
from flaskr import admin_user
from flaskr import admin_posts
from flaskr import admin_content
from flaskr import models
