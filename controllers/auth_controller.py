from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import Usuario
from backend.extensions import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['POST'])
def register():
    dados = request.json

    nome = dados.get("username")
    email = dados.get("email")
    senha = dados.get("password")

    if not nome or not email or not senha:
        return jsonify({"message": "Preencha todos os campos do formulário"}), 400

    usuario: Usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        return jsonify({"message": "Este email já está cadastrado"}), 400

    usuario = Usuario(nome=nome, email=email, senha_hash=generate_password_hash(senha))

    try:
        db.session.add(usuario)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "Erro ao cadastrar usuário"}), 500

    return jsonify({"message": "Usuário cadastrado"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.json

    email = dados.get("email")
    senha = dados.get("password")

    if not email or not senha:
        return jsonify({"message": "Preencha todos os campos do formulário"}), 400

    usuario: Usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({"message": "Email ou senha incorreta"}), 401

    if login_user(usuario):
        return jsonify({"message": "Login realizado"}), 200
    else:
        return jsonify({"message": "Erro ao fazer login"}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "A sessão foi encerrada"}), 200

@auth_bp.route('/me')
def me():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict()), 200

    return jsonify({"message": "Usuário não autenticado"}), 401