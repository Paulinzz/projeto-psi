from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from backend.extensions import db
from backend.utils import noNaive

if TYPE_CHECKING:
    from .contestacao import Contestacao
    from .reclamacao import Reclamacao


class FotoReclamacao(db.Model):
    __tablename__ = 'fotos_reclamacao'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Relacionamento com reclamação
    reclamacao_id: Mapped[int] = mapped_column(
        ForeignKey('reclamacoes.id'),
        nullable=False
    )
    reclamacao: Mapped["Reclamacao"] = relationship(
        "Reclamacao",
        back_populates="fotos"
    )
    
    data_upload: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url, # tirar isso aqui já que expõe a rota da api?
            'nomeArquivo': self.nome_arquivo,
            'dataUpload': self.data_upload.isoformat() if self.data_upload else None
        }


class ProvaContestacao(db.Model):
    __tablename__ = 'provas_contestacao'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Relacionamento com contestação la do contestacao.py que tem as provas
    contestacao_id: Mapped[int] = mapped_column(
        ForeignKey('contestacoes.id'),
        nullable=False
    )
    contestacao: Mapped["Contestacao"] = relationship(
        "Contestacao",
        back_populates="provas"
    )
    
    data_upload: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url, #tirar isso já que expõe a rota da api? 
            'nomeArquivo': self.nome_arquivo,
            'dataUpload': noNaive(self.data_upload).isoformat() if self.data_upload else None
        }