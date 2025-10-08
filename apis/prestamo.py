from typing import List
from uuid import UUID

from crud.prestamo_crud import PrestamoCRUD
from database.config import get_db
from schemas import PrestamoResponse
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

router = APIRouter(prefix="/prestamo", tags=["prestamo"])

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.prestamo_crud import PrestamoCRUD
from database.config import get_db
from schemas import PrestamoResponse

router = APIRouter(prefix="/prestamo", tags=["prestamo"])


@router.get("/", response_model=List[PrestamoResponse])
async def obtener_prestamos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los préstamos con paginación."""
    try:
        prestamo_crud = PrestamoCRUD(db)
        prestamos = prestamo_crud.obtener_todos()
        return prestamos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener préstamo: {str(e)}",
        )


@router.get("/{prestamo_id}", response_model=PrestamoResponse)
async def obtener_prestamo(prestamo_id: UUID, db: Session = Depends(get_db)):
    """Obtener un préstamo por ID."""
    try:
        prestamo_crud = PrestamoCRUD(db)
        prestamo = prestamo_crud.obtener_por_id(prestamo_id)

        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado"
            )

        return prestamo

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener préstamo: {str(e)}",
        )
