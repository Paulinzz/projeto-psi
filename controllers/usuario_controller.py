from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from backend.models import Reclamacao

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/reclamacoes')
@login_required
def usuario_reclamacoes():
    usuario_id = current_user.get_id()
    reclamacoes: list[Reclamacao] = Reclamacao.query.filter(Reclamacao.usuario_id == usuario_id).all()

    return jsonify({"reclamacoes": [r.to_dict() for r in reclamacoes]}), 200