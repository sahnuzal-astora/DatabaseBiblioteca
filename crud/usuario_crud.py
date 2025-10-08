from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from entities.usuario import Usuario  # Asegúrate de que esta ruta sea correcta


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    # 🔹 Obtener todos los usuarios
    def obtener_usuarios(self, skip: int = 0, limit: int = 100):
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    # 🔹 Obtener usuario por ID
    def obtener_usuario(self, usuario_id: UUID):
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    # 🔹 Crear usuario
    def crear_usuario(self, nombre: str, email: str, contrasena_hash: str,
                      telefono: str = None, es_admin: bool = False):
        # Verificar si ya existe el email
        usuario_existente = self.db.query(Usuario).filter(Usuario.email == email).first()
        if usuario_existente:
            raise ValueError("El correo electrónico ya está registrado.")

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            telefono=telefono,
            es_admin=es_admin,
            contrasena_hash=contrasena_hash,
            activo=True,
        )

        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    # 🔹 Actualizar usuario
    def actualizar_usuario(self, usuario_id: UUID, **campos_actualizacion):
        usuario = self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            return None

        for campo, valor in campos_actualizacion.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    # 🔹 Eliminar usuario
    def eliminar_usuario(self, usuario_id: UUID):
        usuario = self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            return False

        self.db.delete(usuario)
        self.db.commit()
        return True

