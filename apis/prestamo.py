"""
Módulo de endpoints para la gestión de préstamos.

Este módulo define las rutas y operaciones relacionadas con los préstamos
en el sistema. Permite consultar todos los préstamos con paginación o
recuperar un préstamo específico por su identificador único (UUID).
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.prestamo_crud import PrestamoCRUD
from database.config import get_db
from schemas import PrestamoResponse

router = APIRouter(prefix="/prestamo", tags=["Préstamos"])


@router.get("/", response_model=List[PrestamoResponse])
async def obtener_prestamos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los préstamos con soporte de paginación.

    Args:
        skip (int, optional): Número de registros a omitir. Por defecto es 0.
        limit (int, optional): Máximo número de préstamos a devolver. Por defecto es 100.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[PrestamoResponse]: Lista de préstamos almacenados en la base de datos.

    Raises:
        HTTPException:
            - 500: Si ocurre un error al obtener los préstamos.
    """
    try:
        prestamo_crud = PrestamoCRUD(db)
        prestamos = prestamo_crud.obtener_todos()
        return prestamos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener préstamos: {str(e)}",
        )


@router.get("/{prestamo_id}", response_model=PrestamoResponse)
async def obtener_prestamo(prestamo_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un préstamo específico por su ID.

    Args:
        prestamo_id (UUID): Identificador único del préstamo.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        PrestamoResponse: Objeto con los detalles del préstamo solicitado.

    Raises:
        HTTPException:
            - 404: Si el préstamo no existe.
            - 500: Si ocurre un error al obtener el préstamo desde la base de datos.
    """
    try:
        prestamo_crud = PrestamoCRUD(db)
        prestamo = prestamo_crud.obtener_por_id(prestamo_id)

        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Préstamo no encontrado",
            )

        return prestamo

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener préstamo: {str(e)}",
        )
