from typing import List
from uuid import UUID

from crud.mapa_crud import MapaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ( MapaCreate, MapaResponse, MapaUpdate,RespuestaAPI)
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/mapas",
    tags=["Mapas"]
)


@router.get("/", response_model=List[MapaResponse])
async def obtener_mapas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los mapas con paginación."""
    try:
        crud = MapaCRUD(db)
        return crud.obtener_mapas(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mapas: {str(e)}",
        )


@router.get("/{mapa_id}", response_model=MapaResponse)
async def obtener_mapa(mapa_id: UUID, db: Session = Depends(get_db)):
    """Obtener un mapa por ID."""
    try:
        crud = MapaCRUD(db)
        mapa = crud.obtener_mapa(mapa_id)
        if not mapa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mapa no encontrado",
            )
        return mapa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mapa: {str(e)}",
        )


@router.post("/", response_model=MapaResponse, status_code=status.HTTP_201_CREATED)
async def crear_mapa(mapa_data: MapaCreate, db: Session = Depends(get_db)):
    """Crear un nuevo mapa."""
    try:
        crud = MapaCRUD(db)
        return crud.crear_mapa(
            region=mapa_data.region,
            escala=mapa_data.escala,
            tipo=mapa_data.tipo,
            producto_id=mapa_data.producto_id,
            id_usuario_crea=mapa_data.id_usuario_crea,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear mapa: {str(e)}",
        )


@router.put("/{mapa_id}", response_model=MapaResponse)
async def actualizar_mapa(mapa_id: UUID, mapa_data: MapaUpdate, db: Session = Depends(get_db)):
    """Actualizar un mapa existente."""
    try:
        crud = MapaCRUD(db)

        existente = crud.obtener_mapa(mapa_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mapa no encontrado",
            )

        campos_actualizacion = {k: v for k, v in mapa_data.dict().items() if v is not None}

        if not campos_actualizacion:
            return existente

        return crud.actualizar_mapa(mapa_id, **campos_actualizacion)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar mapa: {str(e)}",
        )


@router.delete("/{mapa_id}", response_model=RespuestaAPI)
async def eliminar_mapa(mapa_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un mapa."""
    try:
        crud = MapaCRUD(db)

        existente = crud.obtener_mapa(mapa_id)
        if not existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mapa no encontrado",
            )

        eliminado = crud.eliminar_mapa(mapa_id)
        if eliminado:
            return RespuestaAPI(mensaje="Mapa eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar mapa",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar mapa: {str(e)}",
        )