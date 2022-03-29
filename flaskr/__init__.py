from flask import Flask, render_template
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

@app.errorhandler(404)
def page_not_found(e):
    """ Funcion para manejar el error 404 """
    return render_template("errors/404.html"), 404

from flaskr import routes
