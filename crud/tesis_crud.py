from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.tesis_categoria import Tesis
from entities.usuario import Usuario


class TesisCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_tesis(
        self,
        universidad: str,
        director: str,
        grado_academico: str,
        producto_id: UUID,
        id_usuario_crea: UUID = None,
    ) -> Tesis:
        if not universidad or len(universidad.strip()) == 0:
            raise ValueError("La universidad es obligatoria")
        if len(universidad) > 150:
            raise ValueError("La universidad no puede exceder 150 caracteres")
        if not director or len(director.strip()) == 0:
            raise ValueError("El director es obligatorio")
        if len(director) > 100:
            raise ValueError("El director no puede exceder 100 caracteres")
        if not grado_academico or len(grado_academico.strip()) == 0:
            raise ValueError("El grado académico es obligatorio")
        if len(grado_academico) > 100:
            raise ValueError("El grado académico no puede exceder 100 caracteres")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la tesis"
                )
            id_usuario_crea = admin.id_usuario
        tesis = Tesis(
            universidad=universidad.strip(),
            director=director.strip(),
            grado_academico=grado_academico.strip(),
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(tesis)
        self.db.commit()
        self.db.refresh(tesis)
        return tesis

    def obtener_tesis(self, tesis_id: UUID) -> Optional[Tesis]:
        return self.db.query(Tesis).filter(Tesis.id_tesis == tesis_id).first()

    def obtener_tesis_lista(self, skip: int = 0, limit: int = 100) -> List[Tesis]:
        return self.db.query(Tesis).offset(skip).limit(limit).all()

    def actualizar_tesis(
        self, tesis_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Tesis]:
        tesis = self.obtener_tesis(tesis_id)
        if not tesis:
            return None
        if "universidad" in kwargs:
            universidad = kwargs["universidad"]
            if not universidad or len(universidad.strip()) == 0:
                raise ValueError("La universidad es obligatoria")
            if len(universidad) > 150:
                raise ValueError("La universidad no puede exceder 150 caracteres")
            kwargs["universidad"] = universidad.strip()
        if "director" in kwargs:
            director = kwargs["director"]
            if not director or len(director.strip()) == 0:
                raise ValueError("El director es obligatorio")
            if len(director) > 100:
                raise ValueError("El director no puede exceder 100 caracteres")
            kwargs["director"] = director.strip()
        if "grado_academico" in kwargs:
            grado_academico = kwargs["grado_academico"]
            if not grado_academico or len(grado_academico.strip()) == 0:
                raise ValueError("El grado académico es obligatorio")
            if len(grado_academico) > 100:
                raise ValueError("El grado académico no puede exceder 100 caracteres")
            kwargs["grado_academico"] = grado_academico.strip()
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la tesis"
                )
            id_usuario_edita = admin.id_usuario
        tesis.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(tesis, key):
                setattr(tesis, key, value)
        self.db.commit()
        self.db.refresh(tesis)
        return tesis

    def eliminar_tesis(self, tesis_id: UUID) -> bool:
        tesis = self.obtener_tesis(tesis_id)
        if tesis:
            self.db.delete(tesis)
            self.db.commit()
            return True
        return False
