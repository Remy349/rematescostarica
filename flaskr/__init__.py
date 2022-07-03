import os
import paypalrestsdk
import cloudinary
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from config import Config

load_dotenv()

app = Flask(__name__)

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET")
)

PAYPAL_MODE = os.getenv("PAYPAL_MODE")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

paypalrestsdk.configure({
    "mode": PAYPAL_MODE,
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_CLIENT_SECRET,
})

if Config.SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    Config.SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

if not Config.SQLALCHEMY_DATABASE_URI:
    raise RuntimeError("DATABASE_URI is not set!")
else:
    print("DATABASE_URI is ok!!!")

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Session(app)

@app.errorhandler(404)
def page_not_found(e):
    """ Funcion para manejar el error 404 """
    return render_template("errors/404.html"), 404

from flaskr import routes
from flaskr import auth
from flaskr import paypal
from flaskr import admin_user
from flaskr import models
