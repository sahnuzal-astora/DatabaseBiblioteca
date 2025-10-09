"""
Módulo de endpoints para la gestión de usuarios.

Este archivo define las rutas y operaciones CRUD (crear, leer, actualizar y eliminar)
relacionadas con los usuarios del sistema.
"""

from typing import List
from uuid import UUID
from crud.usuario_crud import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los usuarios con paginación.

    Recupera una lista de usuarios registrados en la base de datos con soporte
    para paginación mediante los parámetros `skip` y `limit`.

    Args:
        skip (int, optional): Número de registros a omitir para la paginación. Por defecto es 0.
        limit (int, optional): Cantidad máxima de usuarios a devolver. Por defecto es 100.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[UsuarioResponse]: Lista de usuarios registrados en la base de datos.

    Raises:
        HTTPException:
            - 500: Si ocurre un error al obtener los usuarios desde la base de datos.
    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuarios = usuario_crud.obtener_usuarios(skip=skip, limit=limit)
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un usuario por su ID.

    Args:
        usuario_id (UUID): Identificador único del usuario.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        UsuarioResponse: Objeto con los datos del usuario solicitado.

    Raises:
        HTTPException:
            - 404: Si el usuario no existe.
            - 500: Si ocurre un error en la consulta a la base de datos.
    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario en la base de datos.

    Args:
        usuario_data (UsuarioCreate): Datos requeridos para crear un nuevo usuario.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        UsuarioResponse: Objeto con la información del usuario creado.

    Raises:
        HTTPException:
            - 400: Si los datos proporcionados son inválidos.
            - 500: Si ocurre un error durante la creación del usuario.
    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.crear_usuario(
            nombre=usuario_data.nombre,
            email=usuario_data.email,
            contrasena_hash=usuario_data.contrasena_hash,
            telefono=usuario_data.telefono,
            es_admin=usuario_data.es_admin,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}",
        )


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: UUID, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar los datos de un usuario existente.

    Args:
        usuario_id (UUID): Identificador único del usuario a actualizar.
        usuario_data (UsuarioUpdate): Campos opcionales a modificar en el usuario.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        UsuarioResponse: Objeto con la información actualizada del usuario.

    Raises:
        HTTPException:
            - 404: Si el usuario no existe.
            - 400: Si los datos proporcionados son inválidos.
            - 500: Si ocurre un error al actualizar el registro.
    """
    try:
        usuario_crud = UsuarioCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in usuario_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return usuario_existente

        usuario_actualizado = usuario_crud.actualizar_usuario(
            usuario_id, **campos_actualizacion
        )
        return usuario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}",
        )


@router.delete("/{usuario_id}", response_model=RespuestaAPI)
async def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Eliminar un usuario de la base de datos.

    Args:
        usuario_id (UUID): Identificador único del usuario a eliminar.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RespuestaAPI: Mensaje de confirmación con el estado de la operación.

    Raises:
        HTTPException:
            - 404: Si el usuario no existe.
            - 500: Si ocurre un error al intentar eliminar el usuario.
    """
    try:
        usuario_crud = UsuarioCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        eliminado = usuario_crud.eliminar_usuario(usuario_id)
        if eliminado:
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}",
        )
