import uuid
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from database.config import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id_prestamo = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    usuario_id = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    producto_id = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )
    fecha_prestamo = Column(DateTime, default=datetime.now)
    fecha_devolucion = Column(DateTime, nullable=True)
    devuelto = Column(Boolean, default=False)

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

    producto = relationship(
        "Producto", back_populates="prestamos", foreign_keys=[producto_id]
    )
    usuario = relationship(
        "Usuario", back_populates="prestamos", foreign_keys=[usuario_id]
    )

    def __repr__(self):
        return f"<Prestamo(id_prestamo={self.id_prestamo}, usuario_id={self.usuario_id}, producto_id={self.producto_id})>"
