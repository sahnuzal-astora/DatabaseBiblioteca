"""
Operaciones CRUD para Producto
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from entities.producto import Producto  
from entities.usuario import Usuario  


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(
        self,
        titulo: str,
        autor: str,
        anio: int,
        id_usuario_crea: UUID,
        id_usuario_edita: UUID = None,
        disponible: bool = True,
    ) -> Producto:
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("El título del producto es obligatorio")
        if len(titulo) > 200:
            raise ValueError("El título no puede exceder 200 caracteres")
        if not autor or len(autor.strip()) == 0:
            raise ValueError("El autor es obligatorio")
        if len(autor) > 150:
            raise ValueError("El autor no puede exceder 150 caracteres")
        if not isinstance(anio, int) or anio < 0:
            raise ValueError("El año debe ser un número positivo")

        usuario_crea = (
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario_crea).first()
        )
        if not usuario_crea:
            raise ValueError("El usuario creador especificado no existe")

        if id_usuario_edita:
            usuario_edita = (
                self.db.query(Usuario)
                .filter(Usuario.id_usuario == id_usuario_edita)
                .first()
            )
            if not usuario_edita:
                raise ValueError("El usuario editor especificado no existe")

        producto = Producto(
            titulo=titulo.strip(),
            autor=autor.strip(),
            anio=anio,
            disponible=disponible,
            id_usuario_crea=id_usuario_crea,
            id_usuario_edita=id_usuario_edita,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, producto_id: UUID) -> Optional[Producto]:
        return (
            self.db.query(Producto).filter(Producto.id_producto == producto_id).first()
        )

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def buscar_productos_por_titulo(self, titulo: str) -> List[Producto]:
        return (
            self.db.query(Producto).filter(Producto.titulo.ilike(f"%{titulo}%")).all()
        )

    def actualizar_producto(
        self, producto_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Producto]:
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None

        if "titulo" in kwargs:
            titulo = kwargs["titulo"]
            if not titulo or len(titulo.strip()) == 0:
                raise ValueError("El título del producto es obligatorio")
            if len(titulo) > 200:
                raise ValueError("El título no puede exceder 200 caracteres")
            kwargs["titulo"] = titulo.strip()

        if "autor" in kwargs:
            autor = kwargs["autor"]
            if not autor or len(autor.strip()) == 0:
                raise ValueError("El autor es obligatorio")
            if len(autor) > 150:
                raise ValueError("El autor no puede exceder 150 caracteres")
            kwargs["autor"] = autor.strip()

        if "anio" in kwargs:
            anio = kwargs["anio"]
            if not isinstance(anio, int) or anio < 0:
                raise ValueError("El año debe ser un número positivo")

        if id_usuario_edita:
            usuario_edita = (
                self.db.query(Usuario)
                .filter(Usuario.id_usuario == id_usuario_edita)
                .first()
            )
            if not usuario_edita:
                raise ValueError("El usuario editor especificado no existe")
            producto.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar_producto(self, producto_id: UUID) -> bool:
        producto = self.obtener_producto(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
