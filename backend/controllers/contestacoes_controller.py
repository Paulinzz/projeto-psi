import shutil
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import (
    Contestacao, 
    Reclamacao, 
    StatusReclamacao, 
    ProvaContestacao
)
from backend.extensions import db
from backend.utils import criar_e_obter_diretorio_contestacao, salvar_imagem

contestacoes_bp = Blueprint('contestacoes', __name__)


# falta testar
@contestacoes_bp.route('/reclamacao/<int:reclamacao_id>/contestar', methods=['POST'])
@login_required
def contestar_reclamacao(reclamacao_id):
    reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)
    
    if reclamacao.status != StatusReclamacao.RESOLVIDA:
        return jsonify({
            'message': 'Só é possível contestar reclamações resolvidas'
        }), 400
    
    dados = request.form
    
    contestacao = Contestacao(
        motivo=dados.get('motivo'),
        reclamacao_id=reclamacao_id,
        usuario_id=current_user.get_id()
    )
    
    reclamacao.status = StatusReclamacao.CONTESTADA
    
    try:
        db.session.add(contestacao)
        db.session.commit()
        # return jsonify({
        #     'message': 'Contestação registrada',
        #     'contestacao': contestacao.to_dict()
        # }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao registrar contestação: {str(e)}'}), 500
    

    arquivos = request.files
    imagens = arquivos.getlist("fotos")
    path = criar_e_obter_diretorio_contestacao(reclamacao.id)

    try:
        for img in imagens:
            filename = salvar_imagem(path, img)
            url = f"/api/uploads/reclamacoes/{reclamacao.id}/{filename}"
            prova_contestacao = ProvaContestacao(url=url, nome_arquivo=filename, contestacao=contestacao)
            db.session.add(prova_contestacao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        shutil.rmtree(path)
        return jsonify({"message": f"Erro ao adicionar as fotos de prova de constestação, a contestação foi adicionada sem imagens: {e}"}), 500

    return jsonify({"message": "Contestação adicionada com sucesso", "contestacao": contestacao.to_dict()}), 201