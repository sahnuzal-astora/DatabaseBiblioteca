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

    

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str


class loginResponse(BaseModel):
    clave: str
    nombre_usuario: UsuarioResponse

    class Config:
        from_attributes = True



# Modelos base para prestamo
# Schema base (atributos comunes)
class PrestamoBase(BaseModel):
    usuario_id: UUID
    producto_id: UUID


# Para crear un préstamo (input al endpoint POST)
class PrestamoCreate(PrestamoBase):
    pass


# Para devolver un préstamo (input al endpoint PUT/PATCH)
class PrestamoUpdate(BaseModel):
    devuelto: bool = True


# Para mostrar datos de un préstamo (output al cliente)
class PrestamoResponse(BaseModel):
    id_prestamo: UUID
    usuario_id: UUID
    producto_id: UUID
    fecha_prestamo: datetime
    devuelto: bool
    
    class Config:
        from_attributes = True

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

class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int

    class Config:
        from_attributes = True

##libro



class LibroBase(BaseModel):
    genero: str = None
    paginas: int = None


class LibroCreate(LibroBase):
    pass


class LibroUpdate(BaseModel):
    genero: Optional[str] = None
    paginas: Optional[int] = None
    id_usuario_edita: Optional[UUID] = None


class LibroResponse(LibroBase):
    id_libro: UUID
    producto_id: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True  

class AudiolibroBase(BaseModel):
    narrador: str = None
    duracion: float = None
    formato: str = None
    producto_id: UUID


class AudiolibroCreate(AudiolibroBase):
    pass


class AudiolibroUpdate(BaseModel):
    narrador: Optional[str] = None
    duracion: Optional[float] = None
    formato: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class AudiolibroResponse(AudiolibroBase):
    id_audiolibro: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None

    class Config:
        from_attributes = True

class ComicBase(BaseModel):
    ilustrador: str = None
    editorial: str = None
    volumen: str = None
    producto_id: UUID


class ComicCreate(ComicBase):
    pass


class ComicUpdate(BaseModel):
    ilustrador: Optional[str] = None
    editorial: Optional[str] = None
    volumen: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class ComicResponse(ComicBase):
    id_comic: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None

    class Config:
        from_attributes = True

class MapaBase(BaseModel):
    region: str = None
    escala: str = None
    tipo: str = None
    producto_id: UUID


class MapaCreate(MapaBase):
    pass


class MapaUpdate(BaseModel):
    region: Optional[str] = None
    escala: Optional[str] = None
    tipo: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class MapaResponse(MapaBase):
    id_mapa: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None

class PeriodicoBase(BaseModel):
    fecha_publicacion: str
    producto_id: UUID

    class config:
        from_attributes = True

# -----------------------------
# Crear periódico
# -----------------------------
class PeriodicoCreate(PeriodicoBase):
    pass


# -----------------------------
# Actualizar periódico
# -----------------------------
class PeriodicoUpdate(BaseModel):
    fecha_publicacion: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


# -----------------------------
# Respuesta periódico
# -----------------------------
class PeriodicoResponse(PeriodicoBase):
    id_periodico: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class config:
        from_attributes = True

# -----------------------------
# Esquema base
# -----------------------------
class RevistaBase(BaseModel):
    edicion: str
    producto_id: UUID


# -----------------------------
# Crear revista
# -----------------------------
class RevistaCreate(RevistaBase):
    pass


# -----------------------------
# Actualizar revista
# -----------------------------
class RevistaUpdate(BaseModel):
    edicion: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


# -----------------------------
# Respuesta revista
# -----------------------------
class RevistaResponse(RevistaBase):
    id_revista: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True

# -----------------------------
# Esquema base
# -----------------------------
class TesisBase(BaseModel):
    universidad: str
    director: str
    grado_academico: str
    producto_id: UUID


# -----------------------------
# Crear tesis
# -----------------------------
class TesisCreate(TesisBase):
    pass


# -----------------------------
# Actualizar tesis
# -----------------------------
class TesisUpdate(BaseModel):
    universidad: Optional[str] = None
    director: Optional[str] = None
    grado_academico: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


# -----------------------------
# Respuesta tesis
# -----------------------------
class TesisResponse(TesisBase):
    id_tesis: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True