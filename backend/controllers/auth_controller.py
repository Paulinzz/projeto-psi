from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User
from backend.extensions import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['POST'])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Este email já está cadastrado"}), 400

    new_user = User(username=username, email=email, password_hash=generate_password_hash(password))

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({"message": "Erro ao cadastrar usuário"}), 400

    return jsonify({"message": "Usuário cadastrado"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Email ou senha incorreta"}), 401

    if login_user(user):
        return jsonify({"message": "Login realizado"}), 200
    else:
        return jsonify({"message": "Erro ao fazer login"}), 400

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "A sessão foi encerrada"}), 200