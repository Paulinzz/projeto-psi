from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User
from backend.extensions import db


reclamacoes_bp = Blueprint('reclamacoes', __name__, url_prefix='/reclamacoes')

@reclamacoes_bp.route('/')
def reclamacoes():
    lista_reclamacoes = { 
        "reclamacoes": [
            {
                "id": 1,
                "autor": "Pedro Victor",
                "titulo": "buraco",
                "descricao": "buraco gigantesco na rua de divanilson",
                "cidade": "Caicó-RN",
                "status": "pendente"
            },
            {
                "id": 2,
                "autor": "Abraão",
                "titulo": "cachorro comendo pneu de motoqueiro",
                "descricao": "tem muito cachorro comendo pneu aqui",
                "cidade": "Caicó-RN",
                "status": "resolvida"
            },
            {
                "id": 3,
                "autor": "Givanilson",
                "titulo": "tão assando gato",
                "descricao": "abraao abriu um churrasco de gato no serrote branco",
                "cidade": "Caicó-RN",
                "status": "contestada"
            }
        ]
    }


    return jsonify(lista_reclamacoes), 200

@reclamacoes_bp.route('/resolvidas')
def reclamacoes_resolvidas():
    lista_reclamacoes = { 
        "reclamacoes": [
            {
                "id": 1,
                "autor": "Pedro Victor",
                "titulo": "buraco",
                "descricao": "buraco gigantesco na rua de divanilson",
                "cidade": "Caicó-RN",
                "status": "resolvida"
            },
            {
                "id": 2,
                "autor": "Abraão",
                "titulo": "cachorro comendo pneu de motoqueiro",
                "descricao": "tem muito cachorro comendo pneu aqui",
                "cidade": "Caicó-RN",
                "status": "resolvida"
            },
            {
                "id": 3,
                "autor": "Givanilson",
                "titulo": "tão assando gato",
                "descricao": "abraao abriu um churrasco de gato no serrote branco",
                "cidade": "Caicó-RN",
                "status": "resolvida"
            }
        ]
    }


    return jsonify(lista_reclamacoes), 200

@reclamacoes_bp.route('/contestadas')
def reclamacoes_contestadas():
    lista_reclamacoes = { 
        "reclamacoes": [
            {
                "id": 1,
                "autor": "Pedro Victor",
                "titulo": "buraco",
                "descricao": "buraco gigantesco na rua de divanilson",
                "cidade": "Caicó-RN",
                "status": "contestada"
            },
            {
                "id": 2,
                "autor": "Abraão",
                "titulo": "cachorro comendo pneu de motoqueiro",
                "descricao": "tem muito cachorro comendo pneu aqui",
                "cidade": "Caicó-RN",
                "status": "contestada"
            },
            {
                "id": 3,
                "autor": "Givanilson",
                "titulo": "tão assando gato",
                "descricao": "abraao abriu um churrasco de gato no serrote branco",
                "cidade": "Caicó-RN",
                "status": "contestada"
            }
        ]
    }


    return jsonify(lista_reclamacoes), 200
@reclamacoes_bp.route('/pendentes')
def reclamacoes_pendentes():
    lista_reclamacoes = { 
        "reclamacoes": [
            {
                "id": 1,
                "autor": "Pedro Victor",
                "titulo": "buraco",
                "descricao": "buraco gigantesco na rua de divanilson",
                "cidade": "Caicó-RN",
                "status": "pendente"
            },
            {
                "id": 2,
                "autor": "Abraão",
                "titulo": "cachorro comendo pneu de motoqueiro",
                "descricao": "tem muito cachorro comendo pneu aqui",
                "cidade": "Caicó-RN",
                "status": "pendente"
            },
            {
                "id": 3,
                "autor": "Givanilson",
                "titulo": "tão assando gato",
                "descricao": "abraao abriu um churrasco de gato no serrote branco",
                "cidade": "Caicó-RN",
                "status": "pendente"
            }
        ]
    }


    return jsonify(lista_reclamacoes), 200