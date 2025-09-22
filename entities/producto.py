import uuid
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    anio = Column(Integer, nullable=False)
    disponible = Column(Boolean, default=True)

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

    prestamos = relationship("Prestamo", back_populates="producto", lazy="dynamic")

    libro = relationship("Libro", back_populates="producto")
    revista = relationship("Revista", back_populates="producto")
    periodico = relationship("Periodico", back_populates="producto")
    audiolibro = relationship("Audiolibro", back_populates="producto")
    comic = relationship("Comic", back_populates="producto", uselist=False)
    mapa = relationship("Mapa", back_populates="producto", uselist=False)
    tesis = relationship("Tesis", back_populates="producto", uselist=False)

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, titulo='{self.titulo}', autor='{self.autor}')>"
