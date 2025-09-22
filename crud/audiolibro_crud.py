from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.audiolibro_categoria import Audiolibro
from entities.usuario import Usuario


class AudiolibroCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_audiolibro(
        self,
        narrador: str,
        duracion: float,
        formato: str,
        producto_id: UUID,
        id_usuario_crea: UUID = None,
    ) -> Audiolibro:
        if not narrador or len(narrador.strip()) == 0:
            raise ValueError("El narrador es obligatorio")
        if len(narrador) > 100:
            raise ValueError("El narrador no puede exceder 100 caracteres")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValueError("La duración debe ser positiva")
        if not formato or len(formato.strip()) == 0:
            raise ValueError("El formato es obligatorio")
        if len(formato) > 20:
            raise ValueError("El formato no puede exceder 20 caracteres")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el audiolibro"
                )
            id_usuario_crea = admin.id_usuario
        audiolibro = Audiolibro(
            narrador=narrador.strip(),
            duracion=duracion,
            formato=formato.strip(),
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(audiolibro)
        self.db.commit()
        self.db.refresh(audiolibro)
        return audiolibro

    def obtener_audiolibro(self, audiolibro_id: UUID) -> Optional[Audiolibro]:
        return (
            self.db.query(Audiolibro)
            .filter(Audiolibro.id_audiolibro == audiolibro_id)
            .first()
        )

    def obtener_audiolibros(self, skip: int = 0, limit: int = 100) -> List[Audiolibro]:
        return self.db.query(Audiolibro).offset(skip).limit(limit).all()

    def actualizar_audiolibro(
        self, audiolibro_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Audiolibro]:
        audiolibro = self.obtener_audiolibro(audiolibro_id)
        if not audiolibro:
            return None
        if "narrador" in kwargs:
            narrador = kwargs["narrador"]
            if not narrador or len(narrador.strip()) == 0:
                raise ValueError("El narrador es obligatorio")
            if len(narrador) > 100:
                raise ValueError("El narrador no puede exceder 100 caracteres")
            kwargs["narrador"] = narrador.strip()
        if "duracion" in kwargs:
            duracion = kwargs["duracion"]
            if not isinstance(duracion, (int, float)) or duracion <= 0:
                raise ValueError("La duración debe ser positiva")
        if "formato" in kwargs:
            formato = kwargs["formato"]
            if not formato or len(formato.strip()) == 0:
                raise ValueError("El formato es obligatorio")
            if len(formato) > 20:
                raise ValueError("El formato no puede exceder 20 caracteres")
            kwargs["formato"] = formato.strip()
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el audiolibro"
                )
            id_usuario_edita = admin.id_usuario
        audiolibro.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(audiolibro, key):
                setattr(audiolibro, key, value)
        self.db.commit()
        self.db.refresh(audiolibro)
        return audiolibro

    def eliminar_audiolibro(self, audiolibro_id: UUID) -> bool:
        audiolibro = self.obtener_audiolibro(audiolibro_id)
        if audiolibro:
            self.db.delete(audiolibro)
            self.db.commit()
            return True
        return False
