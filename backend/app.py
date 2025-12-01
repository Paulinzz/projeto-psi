from flask import Flask
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
from backend.extensions import init_db, init_env, db, login_manager
from flask import Blueprint

init_env()
load_dotenv("../.env")

FRONTEND_URL = getenv("FRONTEND_URL")

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE")

CORS(app, resources={r"/*": {"origins": FRONTEND_URL}}, supports_credentials=True)
login_manager.init_app(app)
db.init_app(app)
init_db(app)

api_bp = Blueprint('api', __name__, url_prefix='/api') # todas as rotas começam com /api
from backend.controllers.auth_controller import auth_bp
from backend.controllers.reclamacoes_controller import reclamacoes_bp
from backend.controllers.contestacoes_controller import contestacoes_bp
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(reclamacoes_bp)
api_bp.register_blueprint(contestacoes_bp)

app.register_blueprint(api_bp)
