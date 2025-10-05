"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Modelos base para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str


class loginResponse(BaseModel):
    clave: str
    nombre_usuario: UsuarioResponse


# Modelos base para prestamo
# Schema base (atributos comunes)
class PrestamoBase(BaseModel):
    usuario_id: UUID
    producto_id: UUID


# Para crear un préstamo (input al endpoint POST)
class PrestamoCreate(PrestamoBase):
    usuario_crea_id: Optional[UUID] = None


# Para devolver un préstamo (input al endpoint PUT/PATCH)
class PrestamoUpdate(BaseModel):
    devuelto: bool = True
    usuario_edita_id: Optional[UUID] = None


# Para mostrar datos de un préstamo (output al cliente)
class PrestamoResponse(BaseModel):
    id_prestamo: UUID
    usuario_id: UUID
    producto_id: UUID
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    devuelto: bool
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None

#modelos para productos

# Base (atributos comunes)
class ProductoBase(BaseModel):
    titulo: str 
    autor: str 
    anio: int 
    disponible: bool = True


# Crear producto (input POST)
class ProductoCreate(ProductoBase):
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None


# Actualizar producto (input PUT/PATCH)
class ProductoUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    anio: Optional[int] = None
    disponible: Optional[bool] = None
    id_usuario_edita: Optional[UUID] = None


# Respuesta al cliente (output)
class ProductoResponse(BaseModel):
    id_producto: UUID
    titulo: str
    autor: str
    anio: int
    disponible: bool
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int