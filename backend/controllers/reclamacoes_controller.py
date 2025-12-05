import shutil
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, timezone
from backend.models import StatusReclamacao, Reclamacao, FotoReclamacao
from backend.extensions import db
from backend.utils import (
    criar_e_obter_diretorio_contestacao, 
    criar_e_obter_diretorio_reclamacao,
    salvar_imagem,
    RECLAMACOES_PATH, 
    CONTESTACOES_PATH
)


reclamacoes_bp = Blueprint('reclamacoes', __name__)

@reclamacoes_bp.route('/reclamacao/adicionar', methods=["GET"])
def get_adicionar_reclamacao():
    return jsonify({"max_imagens": 5}), 200


# RECLAMAÇÃO INDIVIDUAL

# @reclamacoes_bp.route('/reclamacao/<int:reclamacao_id>/atualizar', methods=['POST'])
# @login_required
# def atualizar_reclamacao(reclamacao_id):
#     reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

#     dados = request.form

#     if current_user.get_id() != reclamacao.usuario_id:
#         return jsonify({"message": "Apenas o autor da reclamação pode atualiza-la"}), 401
    

#     titulo = dados.get("titulo")
#     descricao = dados.get("descricao")
#     cidade = dados.get("cidade")
#     endereco = dados.get("endereco")

#     try:
#         if titulo and titulo != reclamacao.titulo:
#             reclamacao.titulo = titulo
#         if descricao and descricao != reclamacao.descricao:
#             reclamacao.descricao = descricao
#         if cidade and cidade != reclamacao.cidade:
#             reclamacao.cidade = cidade
#         if endereco and endereco != reclamacao.endereco:
#             reclamacao.endereco = endereco
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": f"Erro ao atualizar dados da reclamação: {e}"}), 500

    
#     arquivos = request.files
#     imagens = arquivos.getlist("fotos")
#     if imagens and imagens[0].filename:
#         if len(reclamacao.fotos) + len(imagens) >= 5:
#             return jsonify({"message": "O limite de 5 imagens foi atingido"}), 400

#         path = criar_e_obter_diretorio_reclamacao(reclamacao.id)
#         try:
#             for img in imagens:
#                 filename = salvar_imagem(path, img)
#                 url = f"/api/uploads/reclamacoes/{reclamacao.id}/{filename}"
#                 prova_reclamacao = FotoReclamacao(url=url, nome_arquivo=filename, reclamacao=reclamacao)
#                 db.session.add(prova_reclamacao)
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             # apagar as imagens do upload
#             return jsonify({"message": f"Erro ao adicionar as fotos da reclamação: {e}"}), 500

#     return jsonify({"message": "Contestação atualizada com sucesso", "reclamacao": reclamacao.to_dict()}), 200

@reclamacoes_bp.route('/reclamacao/<int:reclamacao_id>')
def get_reclamacao(reclamacao_id):
    reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

    return jsonify({"reclamacao": reclamacao.to_dict()}), 200

@reclamacoes_bp.route('/reclamacao/<int:reclamacao_id>/resolver', methods=["POST"])
@login_required
def resolver_reclamacao(reclamacao_id):
    reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

    usuario_id = current_user.get_id()
    if usuario_id != reclamacao.usuario_id:
        return jsonify({"message": "Apenas o autor da reclamação pode resolve-la"}), 401
    if reclamacao.status == StatusReclamacao.RESOLVIDA:
        return jsonify({"message": "Esta reclamação já está resolvida"}), 400
    if reclamacao.status == StatusReclamacao.CONTESTADA:
        return jsonify({"message": "Não é possível resolver uma reclamação contestada"}), 400

    try:
        reclamacao.status = StatusReclamacao.RESOLVIDA
        reclamacao.data_resolucao = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({"message": "Reclamação resolvida com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao resolver reclamação: {e}"}), 500

@reclamacoes_bp.route('/reclamacao/<int:reclamacao_id>/atualizar', methods=["POST"])
@login_required
def atualizar_reclamacao(reclamacao_id):
    reclamacao: Reclamacao = Reclamacao.query.get_or_404(reclamacao_id)

    usuario_id = current_user.get_id()
    if usuario_id != reclamacao.usuario_id:
        return jsonify({"message": "Apenas o autor da reclamação pode atualizá-la"}), 401

    dados = request.form
    arquivos = request.files

    
    titulo = dados.get("titulo")
    descricao = dados.get("descricao")
    cidade = dados.get("cidade")
    endereco = dados.get("endereco")
    try:
        if titulo:
            reclamacao.titulo = titulo
        if descricao:
            reclamacao.descricao = descricao
        if cidade:
            reclamacao.cidade = cidade
        if endereco:
            reclamacao.endereco = endereco
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar dados da reclamação: {e}"}), 500
    
    imagens = arquivos.getlist("fotos") if arquivos else []
    if imagens and imagens[0].filename:
        total_fotos = len(reclamacao.fotos) + len(imagens)
        if total_fotos > 5:
            return jsonify({"message": "Máximo de 5 imagens permitidas"}), 400

        path = criar_e_obter_diretorio_reclamacao(reclamacao.id)

        try:
            for img in imagens:
                if img.filename:
                    filename = salvar_imagem(path, img)
                    url = f"/api/uploads/reclamacoes/{reclamacao.id}/{filename}"
                    foto_reclamacao = FotoReclamacao(url=url, nome_arquivo=filename, reclamacao=reclamacao)
                    db.session.add(foto_reclamacao)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Erro ao adicionar as fotos: {e}"}), 500

    return jsonify({
        "message": "Reclamação atualizada com sucesso",
        "reclamacao": reclamacao.to_dict()
    }), 200

@reclamacoes_bp.route('/reclamacao/adicionar', methods=["POST"])
@login_required
def add_reclamacao():
    dados = request.form
    arquivos = request.files
    # obrigatorios
    titulo = dados.get("titulo")
    descricao = dados.get("descricao")
    cidade = dados.get("cidade")
    # opcionais
    endereco = dados.get("endereco")
    # latitude = dados.get("latitude")
    # longitude = dados.get("longitude")

    if not titulo or not descricao or not cidade:
        return jsonify({"message": "Preencha todos os campos obrigatórios: título, cidade, descrição,"}), 400
    
    usuario_id = current_user.get_id()

    reclamacao = Reclamacao(
        titulo=titulo, 
        descricao=descricao, 
        cidade=cidade, 
        usuario_id=usuario_id, 
        endereco=endereco, 
        # latitude=latitude, 
        # longitude=longitude
    )

    # A RECLAMAÇÃO É CRIADA MESMO QUE OCORRA ERRO AO SALVAR AS FOTOS
    # TROCAR ISSO DEPOIS?
    try:
        db.session.add(reclamacao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao adicionar reclamação: {e}"}), 500

    imagens = arquivos.getlist("fotos")
    path = criar_e_obter_diretorio_reclamacao(reclamacao.id)

    try:
        for img in imagens:
            filename = salvar_imagem(path, img)
            url = f"/api/uploads/reclamacoes/{reclamacao.id}/{filename}"
            foto_reclamacao = FotoReclamacao(url=url, nome_arquivo=filename, reclamacao=reclamacao)
            db.session.add(foto_reclamacao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        shutil.rmtree(path)
        return jsonify({"message": f"Erro ao adicionar as fotos da reclamação: {e}"}), 500

    return jsonify({"message": "Reclamação adicionada com sucesso", "reclamacao": reclamacao.to_dict()}), 201


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