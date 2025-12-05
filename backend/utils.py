import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from secrets import token_hex
from datetime import datetime, timezone


def noNaive(date: datetime):
    "Impede que a data não tenha um timezone, forçando a utilizar o timezone utc +00:00 ou Z"
    if date.tzinfo is None:
        return date.replace(tzinfo=timezone.utc)
    return date


UPLOAD_PATH = "./uploads"
FOTOS_PATH = f"{UPLOAD_PATH}/fotos"
RECLAMACOES_PATH = f"{FOTOS_PATH}/reclamacoes"
CONTESTACOES_PATH = f"{FOTOS_PATH}/contestacoes"

def criar_diretorios_upload():
    UPLOAD_PATHS = [
        UPLOAD_PATH,
        FOTOS_PATH,
        RECLAMACOES_PATH,
        CONTESTACOES_PATH
    ]
    for path in UPLOAD_PATHS:
        if not os.path.exists(path):
            os.mkdir(path)

def criar_e_obter_diretorio_reclamacao(reclamacao_id: str | int) -> str:
    path = f"{RECLAMACOES_PATH}/{reclamacao_id}"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    
    return path

def criar_e_obter_diretorio_contestacao(contestacao_id: str | int) -> str:
    path = f"{CONTESTACOES_PATH}/{contestacao_id}"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    
    return path

def salvar_imagem(path: str, arquivo: FileStorage) -> str:
    'Salva a imagem e retorna o nome do arquivo em que foi salva'

    try:
        filename = secure_filename(arquivo.filename)
        if not filename:
            raise Exception("Nome do arquivo inválido")

        # Obter extensão
        _, ext = os.path.splitext(filename)
        if not ext:
            ext = '.jpg'  # Default

        filepath = os.path.join(path, filename)
        if os.path.exists(filepath):
            filename = f"{token_hex(16)}{ext}"
            filepath = os.path.join(path, filename)

        arquivo.save(filepath)
        
        return filename
    except Exception as e:
        raise Exception(f"Erro ao salvar imagem: {e}")