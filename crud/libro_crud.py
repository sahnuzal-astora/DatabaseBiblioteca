

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.libro_categoria import Libro
from entities.usuario import Usuario


class LibroCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_libro(
        self, genero: str, paginas: int, producto_id: UUID, id_usuario_crea: UUID = None
    ) -> Libro:
        if not genero or len(genero.strip()) == 0:
            raise ValueError("El género es obligatorio")
        if len(genero) > 100:
            raise ValueError("El género no puede exceder 100 caracteres")
        if not isinstance(paginas, int) or paginas <= 0:
            raise ValueError("Las páginas deben ser un número positivo")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el libro"
                )
            id_usuario_crea = admin.id_usuario
        libro = Libro(
            genero=genero.strip(),
            paginas=paginas,
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(libro)
        self.db.commit()
        self.db.refresh(libro)
        return libro

    def obtener_libro(self, libro_id: UUID) -> Optional[Libro]:
        return self.db.query(Libro).filter(Libro.id_libro == libro_id).first()

    def obtener_libros(self, skip: int = 0, limit: int = 100) -> List[Libro]:
        return self.db.query(Libro).offset(skip).limit(limit).all()

    def actualizar_libro(
        self, libro_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Libro]:
        libro = self.obtener_libro(libro_id)
        if not libro:
            return None
        if "genero" in kwargs:
            genero = kwargs["genero"]
            if not genero or len(genero.strip()) == 0:
                raise ValueError("El género es obligatorio")
            if len(genero) > 100:
                raise ValueError("El género no puede exceder 100 caracteres")
            kwargs["genero"] = genero.strip()
        if "paginas" in kwargs:
            paginas = kwargs["paginas"]
            if not isinstance(paginas, int) or paginas <= 0:
                raise ValueError("Las páginas deben ser un número positivo")
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el libro"
                )
            id_usuario_edita = admin.id_usuario
        libro.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(libro, key):
                setattr(libro, key, value)
        self.db.commit()
        self.db.refresh(libro)
        return libro

    def eliminar_libro(self, libro_id: UUID) -> bool:
        libro = self.obtener_libro(libro_id)
        if libro:
            self.db.delete(libro)
            self.db.commit()
            return True
        return False
