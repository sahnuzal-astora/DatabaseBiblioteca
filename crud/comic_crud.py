from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.comic_categoria import Comic
from entities.usuario import Usuario


class ComicCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_comic(
        self,
        ilustrador: str,
        editorial: str,
        volumen: str,
        producto_id: UUID,
        id_usuario_crea: UUID = None,
    ) -> Comic:
        if not ilustrador or len(ilustrador.strip()) == 0:
            raise ValueError("El ilustrador es obligatorio")
        if len(ilustrador) > 100:
            raise ValueError("El ilustrador no puede exceder 100 caracteres")
        if not editorial or len(editorial.strip()) == 0:
            raise ValueError("La editorial es obligatoria")
        if len(editorial) > 100:
            raise ValueError("La editorial no puede exceder 100 caracteres")
        if not volumen or len(volumen.strip()) == 0:
            raise ValueError("El volumen es obligatorio")
        if len(volumen) > 50:
            raise ValueError("El volumen no puede exceder 50 caracteres")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el cómic"
                )
            id_usuario_crea = admin.id_usuario
        comic = Comic(
            ilustrador=ilustrador.strip(),
            editorial=editorial.strip(),
            volumen=volumen.strip(),
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(comic)
        self.db.commit()
        self.db.refresh(comic)
        return comic

    def obtener_comic(self, comic_id: UUID) -> Optional[Comic]:
        return self.db.query(Comic).filter(Comic.id_comic == comic_id).first()

    def obtener_comics(self, skip: int = 0, limit: int = 100) -> List[Comic]:
        return self.db.query(Comic).offset(skip).limit(limit).all()

    def actualizar_comic(
        self, comic_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Comic]:
        comic = self.obtener_comic(comic_id)
        if not comic:
            return None
        if "ilustrador" in kwargs:
            ilustrador = kwargs["ilustrador"]
            if not ilustrador or len(ilustrador.strip()) == 0:
                raise ValueError("El ilustrador es obligatorio")
            if len(ilustrador) > 100:
                raise ValueError("El ilustrador no puede exceder 100 caracteres")
            kwargs["ilustrador"] = ilustrador.strip()
        if "editorial" in kwargs:
            editorial = kwargs["editorial"]
            if not editorial or len(editorial.strip()) == 0:
                raise ValueError("La editorial es obligatoria")
            if len(editorial) > 100:
                raise ValueError("La editorial no puede exceder 100 caracteres")
            kwargs["editorial"] = editorial.strip()
        if "volumen" in kwargs:
            volumen = kwargs["volumen"]
            if not volumen or len(volumen.strip()) == 0:
                raise ValueError("El volumen es obligatorio")
            if len(volumen) > 50:
                raise ValueError("El volumen no puede exceder 50 caracteres")
            kwargs["volumen"] = volumen.strip()
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el cómic"
                )
            id_usuario_edita = admin.id_usuario
        comic.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(comic, key):
                setattr(comic, key, value)
        self.db.commit()
        self.db.refresh(comic)
        return comic

    def eliminar_comic(self, comic_id: UUID) -> bool:
        comic = self.obtener_comic(comic_id)
        if comic:
            self.db.delete(comic)
            self.db.commit()
            return True
        return False
