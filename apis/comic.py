from typing import List
from uuid import UUID

from crud.comic_crud import ComicCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ComicCreate, ComicResponse, ComicUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/comics", tags=["Comics"])


@router.get("/", response_model=List[ComicResponse])
async def obtener_comics(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los cómics con paginación."""
    try:
        crud = ComicCRUD(db)
        return crud.obtener_comics(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cómics: {str(e)}",
        )


@router.get("/{comic_id}", response_model=ComicResponse)
async def obtener_comic(comic_id: UUID, db: Session = Depends(get_db)):
    """Obtener un cómic por ID."""
    try:
        crud = ComicCRUD(db)
        comic = crud.obtener_comic(comic_id)
        if not comic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cómic no encontrado",
            )
        return comic
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cómic: {str(e)}",
        )


@router.post("/", response_model=ComicResponse, status_code=status.HTTP_201_CREATED)
async def crear_comic(comic_data: ComicCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cómic."""
    try:
        crud = ComicCRUD(db)
        return crud.crear_comic(
            ilustrador=comic_data.ilustrador,
            editorial=comic_data.editorial,
            volumen=comic_data.volumen,
            producto_id=comic_data.producto_id,
            id_usuario_crea=comic_data.id_usuario_crea,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cómic: {str(e)}",
        )


@router.put("/{comic_id}", response_model=ComicResponse)
async def actualizar_comic(
    comic_id: UUID, comic_data: ComicUpdate, db: Session = Depends(get_db)
):
    """Actualizar un cómic existente."""
    try:
        crud = ComicCRUD(db)

        existente = crud.obtener_comic(comic_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cómic no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in comic_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return existente

        return crud.actualizar_comic(comic_id, **campos_actualizacion)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cómic: {str(e)}",
        )


@router.delete("/{comic_id}", response_model=RespuestaAPI)
async def eliminar_comic(comic_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un cómic."""
    try:
        crud = ComicCRUD(db)

        existente = crud.obtener_comic(comic_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cómic no encontrado",
            )

        eliminado = crud.eliminar_comic(comic_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cómic eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cómic",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cómic: {str(e)}",
        )
