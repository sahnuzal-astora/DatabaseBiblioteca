from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.revista_categoria import Revista
from entities.usuario import Usuario


class RevistaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_revista(
        self, edicion: str, producto_id: UUID, id_usuario_crea: UUID = None
    ) -> Revista:
        if not edicion or len(edicion.strip()) == 0:
            raise ValueError("La edición es obligatoria")
        if len(edicion) > 50:
            raise ValueError("La edición no puede exceder 50 caracteres")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la revista"
                )
            id_usuario_crea = admin.id_usuario
        revista = Revista(
            edicion=edicion.strip(),
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(revista)
        self.db.commit()
        self.db.refresh(revista)
        return revista

    def obtener_revista(self, revista_id: UUID) -> Optional[Revista]:
        return self.db.query(Revista).filter(Revista.id_revista == revista_id).first()

    def obtener_revistas(self, skip: int = 0, limit: int = 100) -> List[Revista]:
        return self.db.query(Revista).offset(skip).limit(limit).all()

    def actualizar_revista(
        self, revista_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Revista]:
        revista = self.obtener_revista(revista_id)
        if not revista:
            return None
        if "edicion" in kwargs:
            edicion = kwargs["edicion"]
            if not edicion or len(edicion.strip()) == 0:
                raise ValueError("La edición es obligatoria")
            if len(edicion) > 50:
                raise ValueError("La edición no puede exceder 50 caracteres")
            kwargs["edicion"] = edicion.strip()
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la revista"
                )
            id_usuario_edita = admin.id_usuario
        revista.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(revista, key):
                setattr(revista, key, value)
        self.db.commit()
        self.db.refresh(revista)
        return revista

    def eliminar_revista(self, revista_id: UUID) -> bool:
        revista = self.obtener_revista(revista_id)
        if revista:
            self.db.delete(revista)
            self.db.commit()
            return True
        return False
