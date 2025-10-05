from typing import List
from uuid import UUID

from crud.tesis_crud import TesisCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ( TesisCreate, TesisResponse, TesisUpdate, RespuestaAPI )
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/tesis",
    tags=["Tesis"]
)


@router.get("/", response_model=List[TesisResponse])
async def obtener_tesis_lista(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todas las tesis con paginación."""
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
    """Obtener una tesis por ID."""
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
    """Crear una nueva tesis."""
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
async def actualizar_tesis(tesis_id: UUID, tesis_data: TesisUpdate, db: Session = Depends(get_db)):
    """Actualizar una tesis existente."""
    try:
        crud = TesisCRUD(db)

        existente = crud.obtener_tesis(tesis_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tesis no encontrada",
            )

        campos_actualizacion = {k: v for k, v in tesis_data.dict().items() if v is not None}

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
    """Eliminar una tesis."""
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