from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Mapa(Base):
    __tablename__ = "mapas"

    id_mapa = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    region = Column(String(100), nullable=False)
    escala = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=False)
    producto_id = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )

    producto = relationship(
        "Producto", back_populates="mapa", foreign_keys=[producto_id]
    )

    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita,producto"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea,producto"
    )

    def __repr__(self):
        return f"<Mapa(id_mapa={self.id_mapa}, region='{self.region}', escala='{self.escala}', tipo='{self.tipo}')>"
