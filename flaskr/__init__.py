import os
import vimeo
import cloudinary
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from config import Config
from flask_moment import Moment

load_dotenv()

app = Flask(__name__)

if not Config.SQLALCHEMY_DATABASE_URI:
    raise RuntimeError("DATABASE_URI is not set!")
else:
    print("DATABASE_URI is ok!!!")

app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = "flaskr/static/videos"

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

client = vimeo.VimeoClient(
    token=os.getenv("VIMEO_ACCESS_TOKEN"),
    key=os.getenv("VIMEO_CLIENT_ID"),
    secret=os.getenv("VIMEO_CLIENT_SECRET")
)

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
from flaskr import admin_user
from flaskr import admin_posts
from flaskr import admin_content
from flaskr import paypal
from flaskr import models
