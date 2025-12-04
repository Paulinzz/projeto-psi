import shutil
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import Contestacao, Reclamacao, StatusReclamacao, ProvaContestacao
from backend.extensions import db
from backend.utils import (
    criar_e_obter_diretorio_contestacao,
    salvar_imagem,
    CONTESTACOES_PATH
)

contestacoes_bp = Blueprint('contestacoes', __name__)

@contestacoes_bp.route('/usuario/contestacoes')
@login_required
def get_contestacoes_usuario():
    usuario_id = current_user.get_id()
    contestacoes = Contestacao.query.filter_by(usuario_id=usuario_id).all()
    contestacoes_to_dict = [contestacao.to_dict() for contestacao in contestacoes]

    return jsonify({"contestacoes": contestacoes_to_dict}), 200

@contestacoes_bp.route('/reclamacao/<int:reclamacao_id>/contestacoes')
def get_contestacoes_reclamacao(reclamacao_id):
    reclamacao = Reclamacao.query.get_or_404(reclamacao_id)
    contestacoes_to_dict = [contestacao.to_dict() for contestacao in reclamacao.contestacoes]

    return jsonify({"contestacoes": contestacoes_to_dict}), 200

@contestacoes_bp.route('/contestacao/<int:contestacao_id>')
def get_contestacao(contestacao_id):
    contestacao = Contestacao.query.get_or_404(contestacao_id)

    return jsonify({"contestacao": contestacao.to_dict()}), 200

@contestacoes_bp.route('/reclamacao/<int:reclamacao_id>/contestar', methods=['POST'])
@login_required
def contestar_reclamacao(reclamacao_id):
    reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

    if reclamacao.status != StatusReclamacao.RESOLVIDA:
        return jsonify({
            'message': 'Só é possível contestar reclamações resolvidas'
        }), 400

    dados = request.form
    arquivos = request.files

    motivo = dados.get('motivo')
    if not motivo:
        return jsonify({"message": "Motivo é obrigatório"}), 400

    contestacao = Contestacao(
        motivo=motivo,
        reclamacao_id=reclamacao_id,
        usuario_id=current_user.id
    )

    reclamacao.status = StatusReclamacao.CONTESTADA

    try:
        db.session.add(contestacao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar contestação: {e}"}), 500

    imagens = arquivos.getlist("provas")
    if len(imagens) > 5:
        db.session.delete(contestacao)
        db.session.commit()
        return jsonify({"message": "Máximo de 5 imagens permitidas"}), 400

    path = criar_e_obter_diretorio_contestacao(contestacao.id)

    try:
        for img in imagens:
            if img.filename:  # Verifica se há arquivo
                filename = salvar_imagem(path, img)
                url = f"/api/uploads/contestacoes/{contestacao.id}/{filename}"
                prova = ProvaContestacao(url=url, nome_arquivo=filename, contestacao=contestacao)
                db.session.add(prova)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        shutil.rmtree(path)
        return jsonify({"message": f"Erro ao salvar as provas: {e}"}), 500

    return jsonify({
        'message': 'Contestação registrada com sucesso',
        'contestacao': contestacao.to_dict()
    }), 201

@contestacoes_bp.route('/contestacao/<int:contestacao_id>/atualizar', methods=['POST'])
@login_required
def atualizar_contestacao(contestacao_id):
    contestacao = Contestacao.query.get_or_404(contestacao_id)

    if contestacao.usuario_id != current_user.get_id():
        return jsonify({"message": "Apenas o autor da contestação pode atualizá-la"}), 401

    dados = request.form
    arquivos = request.files

    motivo = dados.get('motivo')
    if motivo:
        contestacao.motivo = motivo

    imagens = arquivos.getlist("provas") if arquivos else []

    total_provas = len(contestacao.provas) + len(imagens)
    if total_provas > 5:
        return jsonify({"message": "Máximo de 5 imagens permitidas"}), 400

    path = criar_e_obter_diretorio_contestacao(contestacao.id)

    try:
        for img in imagens:
            if img.filename:
                filename = salvar_imagem(path, img)
                url = f"/api/uploads/contestacoes/{contestacao.id}/{filename}"
                prova = ProvaContestacao(url=url, nome_arquivo=filename, contestacao=contestacao)
                db.session.add(prova)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar as provas: {e}"}), 500

    return jsonify({
        'message': 'Contestação atualizada com sucesso',
        'contestacao': contestacao.to_dict()
    }), 200