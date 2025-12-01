from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from backend.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reclamacao import Reclamacao
    from .contestacao import Contestacao

# utilizando UserMixin para integração com Flask-Login no projetinho
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    reclamacoes: Mapped[list["Reclamacao"]] = relationship(
        "Reclamacao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    
    contestacoes: Mapped[list["Contestacao"]] = relationship(
        "Contestacao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }