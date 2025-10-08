"""
Módulo de endpoints para la gestión de tesis.

Este archivo define las rutas y operaciones relacionadas con el modelo de Tesis,
incluyendo creación, lectura, actualización y eliminación (CRUD).
"""

from typing import List
from uuid import UUID
from crud.tesis_crud import TesisCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import TesisCreate, TesisResponse, TesisUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tesis", tags=["Tesis"])


@router.get("/", response_model=List[TesisResponse])
async def obtener_tesis_lista(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las tesis con paginación.

    Recupera una lista de tesis registradas en la base de datos, con la opción
    de limitar el número de resultados y omitir los primeros registros.

    Args:
        skip (int, optional): Número de registros a omitir para paginación. Por defecto es 0.
        limit (int, optional): Límite máximo de registros a devolver. Por defecto es 100.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[TesisResponse]: Lista de objetos de tipo `TesisResponse` con la información de cada tesis.

    Raises:
        HTTPException: Si ocurre un error al obtener los registros desde la base de datos.
    """
    try:
        crud = TesisCRUD(db)
        return crud.obtener_tesis_lista(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tesis: {str(e)}",
        )


@router.get("/{tesis_id}", response_model=TesisResponse)
async def obtener_tesis(tesis_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener una tesis por su ID.

    Args:
        tesis_id (UUID): Identificador único de la tesis.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        TesisResponse: Objeto con los datos de la tesis solicitada.

    Raises:
        HTTPException:
            - 404: Si la tesis no existe.
            - 500: Si ocurre un error en la consulta a la base de datos.
    """
    try:
        crud = TesisCRUD(db)
        tesis = crud.obtener_tesis(tesis_id)
        if not tesis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tesis no encontrada",
            )
        return tesis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tesis: {str(e)}",
        )


@router.post("/", response_model=TesisResponse, status_code=status.HTTP_201_CREATED)
async def crear_tesis(tesis_data: TesisCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva tesis en la base de datos.

    Args:
        tesis_data (TesisCreate): Datos requeridos para crear una nueva tesis.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        TesisResponse: Objeto con la información de la tesis creada.

    Raises:
        HTTPException:
            - 400: Si los datos proporcionados son inválidos.
            - 500: Si ocurre un error durante la creación del registro.
    """
    try:
        crud = TesisCRUD(db)
        return crud.crear_tesis(
            universidad=tesis_data.universidad,
            director=tesis_data.director,
            grado_academico=tesis_data.grado_academico,
            producto_id=tesis_data.producto_id,
            id_usuario_crea=tesis_data.id_usuario_crea,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear tesis: {str(e)}",
        )


@router.put("/{tesis_id}", response_model=TesisResponse)
async def actualizar_tesis(
    tesis_id: UUID, tesis_data: TesisUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar los datos de una tesis existente.

    Args:
        tesis_id (UUID): Identificador único de la tesis a actualizar.
        tesis_data (TesisUpdate): Campos opcionales a modificar en la tesis.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        TesisResponse: Objeto con la información actualizada de la tesis.

    Raises:
        HTTPException:
            - 404: Si la tesis no existe.
            - 400: Si los datos proporcionados no son válidos.
            - 500: Si ocurre un error al actualizar el registro.
    """
    try:
        crud = TesisCRUD(db)

        existente = crud.obtener_tesis(tesis_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tesis no encontrada",
            )

        campos_actualizacion = {
            k: v for k, v in tesis_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return existente

        return crud.actualizar_tesis(tesis_id, **campos_actualizacion)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar tesis: {str(e)}",
        )


@router.delete("/{tesis_id}", response_model=RespuestaAPI)
async def eliminar_tesis(tesis_id: UUID, db: Session = Depends(get_db)):
    """
    Eliminar una tesis de la base de datos.

    Args:
        tesis_id (UUID): Identificador único de la tesis a eliminar.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RespuestaAPI: Mensaje de confirmación con el estado de la operación.

    Raises:
        HTTPException:
            - 404: Si la tesis no existe.
            - 500: Si ocurre un error al intentar eliminar la tesis.
    """
    try:
        crud = TesisCRUD(db)

        existente = crud.obtener_tesis(tesis_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tesis no encontrada",
            )

        eliminado = crud.eliminar_tesis(tesis_id)
        if eliminado:
            return RespuestaAPI(mensaje="Tesis eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar tesis",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar tesis: {str(e)}",
        )
