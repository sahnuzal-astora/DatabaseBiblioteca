from datetime import datetime
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    contrasena_hash: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None


class UsuarioLogin(BaseModel):
    nombre: str
    contrasena_hash: str


class CambioContrasena(BaseModel):
    contrasena_hash_actual: str
    nueva_contrasena_hash: str


class loginResponse(BaseModel):
    clave: str
    nombre: UsuarioResponse

    class Config:
        from_attributes = True


class PrestamoBase(BaseModel):
    usuario_id: UUID
    producto_id: UUID


class PrestamoCreate(PrestamoBase):
    pass


class PrestamoUpdate(BaseModel):
    devuelto: bool = True


class PrestamoResponse(BaseModel):
    id_prestamo: UUID
    usuario_id: UUID
    producto_id: UUID
    fecha_prestamo: datetime
    devuelto: bool

    class Config:
        from_attributes = True


class ProductoBase(BaseModel):
    titulo: str
    autor: str
    anio: int
    disponible: bool = True


class ProductoCreate(ProductoBase):
    id_usuario_crea: UUID


class ProductoUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    anio: Optional[int] = None
    disponible: Optional[bool] = None
    id_usuario_edita: Optional[UUID] = None


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


class LibroBase(BaseModel):
    genero: str = None
    paginas: int = None
    producto_id: UUID


class LibroCreate(LibroBase):
    id_usuario_crea: UUID


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
    id_usuario_crea: UUID


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
    id_usuario_crea: UUID


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
    id_usuario_crea: UUID


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


class PeriodicoCreate(PeriodicoBase):
    id_usuario_crea: UUID


class PeriodicoUpdate(BaseModel):
    fecha_publicacion: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class PeriodicoResponse(PeriodicoBase):
    id_periodico: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class config:
        from_attributes = True


class RevistaBase(BaseModel):
    edicion: str
    producto_id: UUID


class RevistaCreate(RevistaBase):
    id_usuario_crea: UUID


class RevistaUpdate(BaseModel):
    edicion: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class RevistaResponse(RevistaBase):
    id_revista: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True


class TesisBase(BaseModel):
    universidad: str
    director: str
    grado_academico: str
    producto_id: UUID


class TesisCreate(TesisBase):
    id_usuario_crea: UUID


class TesisUpdate(BaseModel):
    universidad: Optional[str] = None
    director: Optional[str] = None
    grado_academico: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class TesisResponse(TesisBase):
    id_tesis: UUID
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
