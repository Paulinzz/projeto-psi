from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, DateTime, ForeignKey
from backend.extensions import db
from backend.models.foto import ProvaContestacao
from backend.models.reclamacao import Reclamacao
from backend.models.user import User


class Contestacao(db.Model):
    __tablename__ = 'contestacoes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    motivo: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Relacionamento com reclamacao
    reclamacao_id: Mapped[int] = mapped_column(
        ForeignKey('reclamacoes.id'),
        nullable=False
    )
    reclamacao: Mapped["Reclamacao"] = relationship(
        "Reclamacao",
        back_populates="contestacoes"
    )
    
    # Relacionamento com usuário que contestou a reclamacao 
    usuario_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    usuario: Mapped["User"] = relationship("User", back_populates="contestacoes")
    
    # Timestamp (data da contestação)
    data_contestacao: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamento com provas da pessoa que enviou a contestacao(fotos)
    provas: Mapped[list["ProvaContestacao"]] = relationship(
        "ProvaContestacao",
        back_populates="contestacao",
        cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'motivo': self.motivo,
            'reclamacao_id': self.reclamacao_id,
            'usuario_id': self.usuario_id,
            'autor': self.usuario.username,
            'data_contestacao': self.data_contestacao.isoformat() if self.data_contestacao else None,
            'provas': [prova.to_dict() for prova in self.provas]
        }