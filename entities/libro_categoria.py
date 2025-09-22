from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Libro(Base):
    __tablename__ = "libros"

    id_libro = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    genero = Column(String(100), nullable=False)
    paginas = Column(Integer, nullable=False)
    producto_id = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )

    producto = relationship(
        "Producto", back_populates="libro", foreign_keys=[producto_id]
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
        return f"<Libro(id_libro={self.id_libro}, genero='{self.genero}', paginas={self.paginas})>"
