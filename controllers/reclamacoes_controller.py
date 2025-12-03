from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import StatusReclamacao, Reclamacao
from backend.extensions import db

reclamacoes_bp = Blueprint('reclamacoes', __name__)

# RECLAMAÇÃO INDIVIDUAL

@reclamacoes_bp.route('/reclamacao/<int:reclamacao_id>')
def get_reclamacao(reclamacao_id):
    reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

    return jsonify({"reclamacao": reclamacao.to_dict()}), 200

@reclamacoes_bp.route('/reclamacao/adicionar', methods=["POST"])
@login_required
def add_reclamacao():
    dados = request.json

    # obrigatorios
    titulo = dados.get("titulo")
    descricao = dados.get("descricao")
    cidade = dados.get("cidade")
    # opcionais
    endereco = dados.get("endereco")
    latitude = dados.get("latitude")
    longitude = dados.get("longitude")

    usuario_id = current_user.get_id()

    if not titulo or not descricao or not cidade:
        return jsonify({"message": "Preencha todos os campos obrigatórios: título, cidade, descrição,"}), 400
    
    reclamacao = Reclamacao(
        titulo=titulo, 
        descricao=descricao, 
        cidade=cidade, 
        usuario_id=usuario_id, 
        endereco=endereco, 
        latitude=latitude, 
        longitude=longitude
    )

    try:
        db.session.add(reclamacao)
        db.session.commit()
        return jsonify({"message": "Reclamação adicionada com sucesso", "reclamacao": reclamacao.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao adicionar reclamação: {e}"}), 500
    

# LISTAGEM DE RECLAMAÇÕES

@reclamacoes_bp.route('/reclamacoes')
def reclamacoes():
    reclamacoes: list[Reclamacao] = Reclamacao.query.all()
    reclamacoes_to_dict = [reclamacao.to_dict() for reclamacao in reclamacoes]

    return jsonify({"reclamacoes": reclamacoes_to_dict}), 200

@reclamacoes_bp.route('/reclamacoes/pendentes')
def reclamacoes_pendentes():
    reclamacoes: list[Reclamacao] = Reclamacao.query.filter(Reclamacao.status == StatusReclamacao.PENDENTE).all()
    reclamacoes_to_dict = [reclamacao.to_dict() for reclamacao in reclamacoes]

    return jsonify({"reclamacoes": reclamacoes_to_dict}), 200

@reclamacoes_bp.route('/reclamacoes/resolvidas')
def reclamacoes_resolvidas():
    reclamacoes: list[Reclamacao] = Reclamacao.query.filter(Reclamacao.status == StatusReclamacao.RESOLVIDA).all()
    reclamacoes_to_dict = [reclamacao.to_dict() for reclamacao in reclamacoes]

    return jsonify({"reclamacoes": reclamacoes_to_dict}), 200

@reclamacoes_bp.route('/reclamacoes/contestadas')
def reclamacoes_contestadas():
    reclamacoes: list[Reclamacao] = Reclamacao.query.filter(Reclamacao.status == StatusReclamacao.CONTESTADA).all()
    reclamacoes_to_dict = [reclamacao.to_dict() for reclamacao in reclamacoes]

    return jsonify({"reclamacoes": reclamacoes_to_dict}), 200