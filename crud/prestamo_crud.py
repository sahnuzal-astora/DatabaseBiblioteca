import logging
from datetime import datetime
from sqlalchemy.orm import Session
from uuid import UUID
from entities.Prestamo import Prestamo
from entities.usuario import Usuario
from entities.producto import Producto

logger = logging.getLogger(__name__)


class PrestamoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_prestamo(self, usuario_id, producto_id, usuario_crea_id=None):

        try:
            usuario = self.db.query(Usuario).filter_by(id_usuario=usuario_id).first()
            producto = (
                self.db.query(Producto).filter_by(id_producto=producto_id).first()
            )

            if not usuario:
                raise ValueError(" Usuario no encontrado")
            if not producto:
                raise ValueError(" Producto no encontrado")
            if not getattr(producto, "disponible", True):
                raise ValueError(" El producto ya está prestado")

            if usuario_crea_id is None:
                usuario_crea_id = usuario_id

            nuevo_prestamo = Prestamo(
                usuario_id=usuario_id,
                producto_id=producto_id,
                fecha_prestamo=datetime.now(),
                devuelto=False,
                id_usuario_crea=usuario_crea_id,
            )

            producto.disponible = False

            self.db.add(nuevo_prestamo)
            self.db.commit()
            self.db.refresh(nuevo_prestamo)

            logger.info(f" Préstamo creado: {nuevo_prestamo}")
            return nuevo_prestamo

        except Exception as e:
            self.db.rollback()
            logger.error(f" Error al crear préstamo: {e}")
            raise

    def devolver_prestamo(self, id_prestamo, usuario_edita_id=None):

        try:

            if isinstance(id_prestamo, str):
                try:
                    id_prestamo = UUID(id_prestamo)
                except ValueError:
                    raise ValueError(f" ID de préstamo inválido: {id_prestamo}")

            prestamo = (
                self.db.query(Prestamo).filter_by(id_prestamo=id_prestamo).first()
            )

            if not prestamo:
                raise ValueError(f" Préstamo no encontrado con id: {id_prestamo}")

            prestamo.devuelto = True
            prestamo.fecha_devolucion = datetime.now()
            if usuario_edita_id:
                prestamo.id_usuario_edita = usuario_edita_id

            producto = (
                self.db.query(Producto)
                .filter_by(id_producto=prestamo.producto_id)
                .first()
            )
            if producto:
                producto.disponible = True

            self.db.commit()
            self.db.refresh(prestamo)

            logger.info(f" Préstamo devuelto: {prestamo}")
            return prestamo

        except Exception as e:
            self.db.rollback()
            logger.error(f" Error al devolver préstamo: {e}")
            raise

    def obtener_prestamos_usuario(
        self, usuario_id: UUID, skip: int = 0, limit: int = 100
    ):
        return (
            self.db.query(Prestamo)
            .filter(Prestamo.usuario_id == usuario_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_todos(self):

        return self.db.query(Prestamo).all()

    def obtener_por_id(self, id_prestamo: UUID):

        return (
            self.db.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
        )
