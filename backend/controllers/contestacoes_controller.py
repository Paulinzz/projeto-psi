from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import Contestacao, Reclamacao, StatusReclamacao
from backend.extensions import db

contestacoes_bp = Blueprint('contestacoes', __name__)

@contestacoes_bp.route('/reclamacao/<int:reclamacao_id>/contestar', methods=['POST'])
@login_required
def contestar_reclamacao(reclamacao_id):
    reclamacao = Reclamacao.query.get_or_404(reclamacao_id)
    
    if reclamacao.status != StatusReclamacao.RESOLVIDA:
        return jsonify({
            'message': 'Só é possível contestar reclamações resolvidas'
        }), 400
    
    dados = request.json
    
    contestacao = Contestacao(
        motivo=dados.get('motivo'),
        reclamacao_id=reclamacao_id,
        usuario_id=current_user.id
    )
    
    reclamacao.status = StatusReclamacao.CONTESTADA
    
    try:
        db.session.add(contestacao)
        db.session.commit()
        return jsonify({
            'message': 'Contestação registrada',
            'contestacao': contestacao.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 400