from flask import Flask
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
from backend.extensions import init_db, init_env, db, login_manager

init_env()
load_dotenv("../.env")

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE")

CORS(app)
login_manager.init_app(app)
db.init_app(app)
init_db(app)

from backend.controllers.auth import auth_bp

app.register_blueprint(auth_bp)