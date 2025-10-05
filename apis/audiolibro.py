from typing import List
from uuid import UUID

from crud.audiolibro_crud import AudiolibroCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ( AudiolibroCreate, AudiolibroResponse,RespuestaAPI, AudiolibroUpdate)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/audiolibro", tags=["audiolibro"])

@router.get("/", response_model=List[AudiolibroResponse])
async def obtener_audiolibros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los audiolibros con paginación."""
    try:
        crud = AudiolibroCRUD(db)
        return crud.obtener_audiolibros(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener audiolibros: {str(e)}",
        )


@router.get("/{audiolibro_id}", response_model=AudiolibroResponse)
async def obtener_audiolibro(audiolibro_id: UUID, db: Session = Depends(get_db)):
    """Obtener un audiolibro por ID."""
    try:
        crud = AudiolibroCRUD(db)
        audiolibro = crud.obtener_audiolibro(audiolibro_id)
        if not audiolibro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audiolibro no encontrado",
            )
        return audiolibro
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener audiolibro: {str(e)}",
        )


@router.post("/", response_model=AudiolibroResponse, status_code=status.HTTP_201_CREATED)
async def crear_audiolibro(audiolibro_data: AudiolibroCreate, db: Session = Depends(get_db)):
    """Crear un nuevo audiolibro."""
    try:
        crud = AudiolibroCRUD(db)
        return crud.crear_audiolibro(
            narrador=audiolibro_data.narrador,
            duracion=audiolibro_data.duracion,
            formato=audiolibro_data.formato,
            producto_id=audiolibro_data.producto_id,
            id_usuario_crea=audiolibro_data.id_usuario_crea,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear audiolibro: {str(e)}",
        )


@router.put("/{audiolibro_id}", response_model=AudiolibroResponse)
async def actualizar_audiolibro(audiolibro_id: UUID, audiolibro_data: AudiolibroUpdate, db: Session = Depends(get_db)):
    """Actualizar un audiolibro existente."""
    try:
        crud = AudiolibroCRUD(db)

        # Verificar existencia
        existente = crud.obtener_audiolibro(audiolibro_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audiolibro no encontrado",
            )

        # Filtrar campos no nulos
        campos_actualizacion = {k: v for k, v in audiolibro_data.dict().items() if v is not None}

        if not campos_actualizacion:
            return existente

        return crud.actualizar_audiolibro(audiolibro_id, **campos_actualizacion)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar audiolibro: {str(e)}",
        )


@router.delete("/{audiolibro_id}", response_model=RespuestaAPI)
async def eliminar_audiolibro(audiolibro_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un audiolibro."""
    try:
        crud = AudiolibroCRUD(db)

        existente = crud.obtener_audiolibro(audiolibro_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audiolibro no encontrado",
            )

        eliminado = crud.eliminar_audiolibro(audiolibro_id)
        if eliminado:
            return RespuestaAPI(mensaje="Audiolibro eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar audiolibro",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar audiolibro: {str(e)}",
        )