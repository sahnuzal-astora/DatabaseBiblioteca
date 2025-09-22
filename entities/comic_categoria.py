from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Comic(Base):
    __tablename__ = "comics"

    id_comic = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    ilustrador = Column(String(100), nullable=False)
    editorial = Column(String(100), nullable=False)
    volumen = Column(String(50), nullable=False)
    producto_id = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )
    producto = relationship(
        "Producto", back_populates="comic", foreign_keys=[producto_id]
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
        return f"<Comic(id_comic={self.id_comic}, ilustrador='{self.ilustrador}', editorial='{self.editorial}', volumen='{self.volumen}')>"
