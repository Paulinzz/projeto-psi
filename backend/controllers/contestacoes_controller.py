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
from backend.utils import (
    criar_e_obter_diretorio_contestacao,
    salvar_imagem,
    CONTESTACOES_PATH
)

contestacoes_bp = Blueprint('contestacoes', __name__)


@contestacoes_bp.route('/reclamacao/<int:reclamacao_id>/contestacoes')
def get_contestacoes_reclamacao(reclamacao_id):
    reclamacao = Reclamacao.query.get_or_404(reclamacao_id)
    contestacoes_to_dict = [contestacao.to_dict() for contestacao in reclamacao.contestacoes]

    return jsonify({"contestacoes": contestacoes_to_dict}), 200

@contestacoes_bp.route('/contestacao/<int:contestacao_id>')
def get_contestacao(contestacao_id):
    contestacao = Contestacao.query.get_or_404(contestacao_id)

    return jsonify({"contestacao": contestacao.to_dict()}), 200

@contestacoes_bp.route('/contestacao/<int:contestacao_id>/atualizar', methods=['POST'])
@login_required
def atualizar_contestacao(contestacao_id):
    contestacao: Contestacao = Contestacao.query.get_or_404(contestacao_id)

    dados = request.form

    if current_user.get_id() != contestacao.usuario_id:
        return jsonify({"message": "Apenas o autor da contestação pode atualiza-la"}), 401
    

    motivo = dados.get("motivo")
    
    try:
        if motivo and motivo != contestacao.motivo:
            contestacao.motivo = motivo
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar dados da contestação: {e}"}), 500

    arquivos = request.files
    imagens = arquivos.getlist("fotos")
    if imagens and imagens[0].filename:
        if len(contestacao.provas) + len(imagens) > 5:
            return jsonify({"message": "O limite de 5 imagens foi atingido"}), 400

        path = criar_e_obter_diretorio_contestacao(contestacao.id)
        try:
            for img in imagens:
                if img.filename:
                    filename = salvar_imagem(path, img)
                    url = f"/api/uploads/contestacoes/{contestacao.id}/{filename}"
                    prova_contestacao = ProvaContestacao(url=url, nome_arquivo=filename, contestacao=contestacao)
                    db.session.add(prova_contestacao)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # apagar as imagens do upload
            return jsonify({"message": f"Erro ao adicionar as fotos de prova de constestação: {e}"}), 500

    return jsonify({"message": "Contestação atualizada com sucesso", "contestacao": contestacao.to_dict()}), 200

@contestacoes_bp.route('/reclamacao/<int:reclamacao_id>/contestar', methods=['POST'])
@login_required
def contestar_reclamacao(reclamacao_id):
    reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

    if reclamacao.status == StatusReclamacao.PENDENTE:
        return jsonify({
            'message': 'Não é possível contestar reclamações pendentes'
        }), 400

    dados = request.form
    arquivos = request.files

    motivo = dados.get('motivo')
    if not motivo:
        return jsonify({"message": "Motivo é obrigatório"}), 400

    contestacao = Contestacao(
        motivo=motivo,
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

    if imagens and imagens[0]:
        path = criar_e_obter_diretorio_contestacao(contestacao.id)
        try:
            for img in imagens:
                if img.filename:
                    filename = salvar_imagem(path, img)
                    url = f"/api/uploads/contestacoes/{contestacao.id}/{filename}"
                    prova_contestacao = ProvaContestacao(url=url, nome_arquivo=filename, contestacao=contestacao)
                    db.session.add(prova_contestacao)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            shutil.rmtree(path)
            return jsonify({"message": f"Erro ao adicionar as fotos de prova de constestação, a contestação foi adicionada sem imagens: {e}"}), 500

    return jsonify({"message": "Contestação adicionada com sucesso", "contestacao": contestacao.to_dict()}), 201