from typing import List
from uuid import UUID

from crud.periodico_crud import PeriodicoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PeriodicoCreate, PeriodicoResponse, PeriodicoUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/periodico", tags=["periodico"])


@router.get("/", response_model=List[PeriodicoResponse])
async def obtener_periodicos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los periódicos con paginación."""
    try:
        crud = PeriodicoCRUD(db)
        return crud.obtener_periodicos(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener periódicos: {str(e)}",
        )


@router.get("/{periodico_id}", response_model=PeriodicoResponse)
async def obtener_periodico(periodico_id: UUID, db: Session = Depends(get_db)):
    """Obtener un periódico por ID."""
    try:
        crud = PeriodicoCRUD(db)
        periodico = crud.obtener_periodico(periodico_id)
        if not periodico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periódico no encontrado",
            )
        return periodico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener periódico: {str(e)}",
        )


@router.post("/", response_model=PeriodicoResponse, status_code=status.HTTP_201_CREATED)
async def crear_periodico(
    periodico_data: PeriodicoCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo periódico."""
    try:
        crud = PeriodicoCRUD(db)
        return crud.crear_periodico(
            fecha_publicacion=periodico_data.fecha_publicacion,
            producto_id=periodico_data.producto_id,
            id_usuario_crea=periodico_data.id_usuario_crea,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear periódico: {str(e)}",
        )


@router.put("/{periodico_id}", response_model=PeriodicoResponse)
async def actualizar_periodico(
    periodico_id: UUID, periodico_data: PeriodicoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un periódico existente."""
    try:
        crud = PeriodicoCRUD(db)

        existente = crud.obtener_periodico(periodico_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periódico no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in periodico_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return existente

        return crud.actualizar_periodico(periodico_id, **campos_actualizacion)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar periódico: {str(e)}",
        )


@router.delete("/{periodico_id}", response_model=RespuestaAPI)
async def eliminar_periodico(periodico_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un periódico."""
    try:
        crud = PeriodicoCRUD(db)

        existente = crud.obtener_periodico(periodico_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periódico no encontrado",
            )

        eliminado = crud.eliminar_periodico(periodico_id)
        if eliminado:
            return RespuestaAPI(mensaje="Periódico eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar periódico",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar periódico: {str(e)}",
        )
