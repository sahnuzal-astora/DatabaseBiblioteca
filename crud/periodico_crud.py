from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.periodico_categoria import Periodico
from entities.usuario import Usuario


class PeriodicoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_periodico(
        self, fecha_publicacion: str, producto_id: UUID, id_usuario_crea: UUID = None
    ) -> Periodico:
        if not fecha_publicacion or len(fecha_publicacion.strip()) == 0:
            raise ValueError("La fecha de publicación es obligatoria")
        if len(fecha_publicacion) > 50:
            raise ValueError("La fecha de publicación no puede exceder 50 caracteres")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el periódico"
                )
            id_usuario_crea = admin.id_usuario
        periodico = Periodico(
            fecha_publicacion=fecha_publicacion.strip(),
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(periodico)
        self.db.commit()
        self.db.refresh(periodico)
        return periodico

    def obtener_periodico(self, periodico_id: UUID) -> Optional[Periodico]:
        return (
            self.db.query(Periodico)
            .filter(Periodico.id_periodico == periodico_id)
            .first()
        )

    def obtener_periodicos(self, skip: int = 0, limit: int = 100) -> List[Periodico]:
        return self.db.query(Periodico).offset(skip).limit(limit).all()

    def actualizar_periodico(
        self, periodico_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Periodico]:
        periodico = self.obtener_periodico(periodico_id)
        if not periodico:
            return None
        if "fecha_publicacion" in kwargs:
            fecha_publicacion = kwargs["fecha_publicacion"]
            if not fecha_publicacion or len(fecha_publicacion.strip()) == 0:
                raise ValueError("La fecha de publicación es obligatoria")
            if len(fecha_publicacion) > 50:
                raise ValueError(
                    "La fecha de publicación no puede exceder 50 caracteres"
                )
            kwargs["fecha_publicacion"] = fecha_publicacion.strip()
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el periódico"
                )
            id_usuario_edita = admin.id_usuario
        periodico.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(periodico, key):
                setattr(periodico, key, value)
        self.db.commit()
        self.db.refresh(periodico)
        return periodico

    def eliminar_periodico(self, periodico_id: UUID) -> bool:
        periodico = self.obtener_periodico(periodico_id)
        if periodico:
            self.db.delete(periodico)
            self.db.commit()
            return True
        return False
