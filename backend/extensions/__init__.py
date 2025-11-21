from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_env():
    from secrets import token_hex
    from os import path


    if not path.exists(".env"):
        variables = f"""
        DATABASE = "sqlite:///database.db"
        SECRET_KEY = "{token_hex()}"
        """
        
        with open(".env", "w") as env:
            env.write(variables)
    

def init_db(app: Flask):
    import backend.models

    with app.app_context():
        db.create_all()


login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = "Faça login para realizar essa ação"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    from backend.models import User

    user = User.query.get(int(user_id))

    return user