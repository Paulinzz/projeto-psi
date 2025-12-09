from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from backend.extensions import init_db, init_env, db, login_manager
from backend.utils import criar_diretorios_upload


criar_diretorios_upload()

init_env()
load_dotenv("../.env")

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE")


FRONTEND_URL = getenv("FRONTEND_URL")
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}}, supports_credentials=True)
login_manager.init_app(app)
db.init_app(app)
init_db(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Não encontrado"}), 404

api_bp = Blueprint('api', __name__, url_prefix='/api') # todas as rotas começam com /api
from backend.controllers.auth_controller import auth_bp
from backend.controllers.reclamacoes_controller import reclamacoes_bp
from backend.controllers.contestacoes_controller import contestacoes_bp
from backend.controllers.uploads_controller import uploads_bp
from backend.controllers.usuario_controller import usuario_bp
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(reclamacoes_bp)
api_bp.register_blueprint(contestacoes_bp)
api_bp.register_blueprint(uploads_bp)
api_bp.register_blueprint(usuario_bp)

app.register_blueprint(api_bp)