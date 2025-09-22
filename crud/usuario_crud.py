"""
Operaciones CRUD para Usuario
"""

import re
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.usuario import Usuario  


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db
        self._crear_admin_por_defecto()  

    def _validar_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def crear_usuario(
        self,
        nombre: str,
        email: str,
        contrasena_hash: str,
        telefono: Optional[str] = None,
        es_admin: bool = False,
    ) -> Usuario:
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")
        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        usuario = Usuario(
            nombre=nombre.strip(),
            email=email.lower().strip(),
            telefono=telefono.strip() if telefono else None,
            es_admin=es_admin,
            contrasena_hash=contrasena_hash,
            activo=True,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_usuario_por_email(email)
                and self.obtener_usuario_por_email(email).id_usuario != usuario_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            if not self._validar_telefono(kwargs["telefono"]):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        return self.db.query(Usuario).filter(Usuario.es_admin == True).all()

    def es_admin(self, usuario_id: UUID) -> bool:
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@system.com", Usuario.es_admin == True)
            .first()
        )

    def autenticar_usuario(self, email: str, contrasena: str):
        usuario = self.obtener_usuario_por_email(email)
        if not usuario or not usuario.activo:
            return None

        from auth.security import PasswordManager

        if PasswordManager.verify_password(contrasena, usuario.contrasena_hash):
            return usuario
        return None

    def _crear_admin_por_defecto(self):
        """
        Crea un usuario administrador por defecto si no existe.
        Email: admin@system.com
        Contraseña: admin123
        """
        from auth.security import PasswordManager

        admin = self.obtener_admin_por_defecto()
        if not admin:
            contrasena_hash = PasswordManager.hash_password("admin123")
            self.crear_usuario(
                nombre="Administrador",
                email="admin@system.com",
                contrasena_hash=contrasena_hash,
                telefono="+573001112233",
                es_admin=True,
            )
            print(" Usuario administrador creado: admin@system.com / admin123")
