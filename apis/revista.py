"""
Módulo de endpoints para la gestión de revistas.

Define las rutas y operaciones CRUD (crear, leer, actualizar y eliminar)
relacionadas con las revistas dentro del sistema.
"""

from typing import List
from uuid import UUID
from crud.revista_crud import RevistaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import RevistaCreate, RevistaResponse, RevistaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/revistas", tags=["Revistas"])


@router.get("/", response_model=List[RevistaResponse])
async def obtener_revistas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las revistas con paginación.

    Recupera una lista de revistas registradas en la base de datos con soporte
    para paginación mediante los parámetros `skip` y `limit`.

    Args:
        skip (int, optional): Número de registros a omitir para la paginación. Por defecto es 0.
        limit (int, optional): Cantidad máxima de revistas a devolver. Por defecto es 100.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[RevistaResponse]: Lista de revistas encontradas en la base de datos.

    Raises:
        HTTPException:
            - 500: Si ocurre un error al obtener las revistas desde la base de datos.
    """
    try:
        crud = RevistaCRUD(db)
        return crud.obtener_revistas(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener revistas: {str(e)}",
        )


@router.get("/{revista_id}", response_model=RevistaResponse)
async def obtener_revista(revista_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener una revista por su ID.

    Args:
        revista_id (UUID): Identificador único de la revista.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RevistaResponse: Objeto con los datos de la revista solicitada.

    Raises:
        HTTPException:
            - 404: Si la revista no existe.
            - 500: Si ocurre un error en la consulta a la base de datos.
    """
    try:
        crud = RevistaCRUD(db)
        revista = crud.obtener_revista(revista_id)
        if not revista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Revista no encontrada",
            )
        return revista
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener revista: {str(e)}",
        )


@router.post("/", response_model=RevistaResponse, status_code=status.HTTP_201_CREATED)
async def crear_revista(revista_data: RevistaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva revista en la base de datos.

    Args:
        revista_data (RevistaCreate): Datos requeridos para crear una nueva revista.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RevistaResponse: Objeto con la información de la revista creada.

    Raises:
        HTTPException:
            - 400: Si los datos proporcionados son inválidos.
            - 500: Si ocurre un error durante la creación del registro.
    """
    try:
        crud = RevistaCRUD(db)
        return crud.crear_revista(
            edicion=revista_data.edicion,
            producto_id=revista_data.producto_id,
            id_usuario_crea=revista_data.id_usuario_crea,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear revista: {str(e)}",
        )


@router.put("/{revista_id}", response_model=RevistaResponse)
async def actualizar_revista(
    revista_id: UUID, revista_data: RevistaUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar los datos de una revista existente.

    Args:
        revista_id (UUID): Identificador único de la revista a actualizar.
        revista_data (RevistaUpdate): Campos opcionales a modificar en la revista.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RevistaResponse: Objeto con la información actualizada de la revista.

    Raises:
        HTTPException:
            - 404: Si la revista no existe.
            - 400: Si los datos proporcionados son inválidos.
            - 500: Si ocurre un error al actualizar el registro.
    """
    try:
        crud = RevistaCRUD(db)

        existente = crud.obtener_revista(revista_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Revista no encontrada",
            )

        campos_actualizacion = {
            k: v for k, v in revista_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return existente

        return crud.actualizar_revista(revista_id, **campos_actualizacion)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar revista: {str(e)}",
        )


@router.delete("/{revista_id}", response_model=RespuestaAPI)
async def eliminar_revista(revista_id: UUID, db: Session = Depends(get_db)):
    """
    Eliminar una revista de la base de datos.

    Args:
        revista_id (UUID): Identificador único de la revista a eliminar.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RespuestaAPI: Mensaje de confirmación con el estado de la operación.

    Raises:
        HTTPException:
            - 404: Si la revista no existe.
            - 500: Si ocurre un error al intentar eliminar la revista.
    """
    try:
        crud = RevistaCRUD(db)

        existente = crud.obtener_revista(revista_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Revista no encontrada",
            )

        eliminado = crud.eliminar_revista(revista_id)
        if eliminado:
            return RespuestaAPI(mensaje="Revista eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar revista",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar revista: {str(e)}",
        )
