from flask import Blueprint, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join
from backend.utils import CONTESTACOES_PATH, RECLAMACOES_PATH


uploads_bp = Blueprint("uploads", __name__)

@uploads_bp.route("/uploads/contestacoes/<int:contestacao_id>/<nome_arquivo>")
def prova_contestacao(contestacao_id, nome_arquivo):
    arquivo_seguro = secure_filename(nome_arquivo)
    diretorio = safe_join(CONTESTACOES_PATH, str(contestacao_id))

    return send_from_directory(diretorio, arquivo_seguro)

@uploads_bp.route("/uploads/reclamacoes/<int:reclamacao_id>/<nome_arquivo>")
def foto_reclamacao(reclamacao_id, nome_arquivo):
    arquivo_seguro = secure_filename(nome_arquivo)
    diretorio = safe_join(RECLAMACOES_PATH, str(reclamacao_id))

    return send_from_directory(diretorio, arquivo_seguro)