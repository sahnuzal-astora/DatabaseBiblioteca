from typing import List
from uuid import UUID

from crud.libro_crud import LibroCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import LibroCreate, LibroResponse, LibroUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/libro", tags=["libro"])


@router.get("/", response_model=List[LibroResponse])
async def obtener_libros(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los libros con paginación."""
    try:
        libro_crud = LibroCRUD(db)
        libros = libro_crud.obtener_libros(skip=skip, limit=limit)
        return libros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener libros: {str(e)}",
        )


@router.get("/{libro_id}", response_model=LibroResponse)
async def obtener_libro(libro_id: UUID, db: Session = Depends(get_db)):
    """Obtener un libro por ID."""
    try:
        libro_crud = LibroCRUD(db)
        libro = libro_crud.obtener_libro(libro_id)
        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado"
            )
        return libro
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener libro: {str(e)}",
        )


@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
async def crear_libro(libro_data: LibroCreate, db: Session = Depends(get_db)):
    """Crear un nuevo libro."""
    try:
        libro_crud = LibroCRUD(db)
        libro = libro_crud.crear_libro(
            genero=libro_data.genero,
            paginas=libro_data.paginas,
            producto_id=libro_data.producto_id,
            id_usuario_crea=libro_data.id_usuario_crea,
        )
        return libro
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear libro: {str(e)}",
        )


@router.put("/{libro_id}", response_model=LibroResponse)
async def actualizar_libro(
    libro_id: UUID, libro_data: LibroUpdate, db: Session = Depends(get_db)
):
    """Actualizar un libro existente."""
    try:
        libro_crud = LibroCRUD(db)

        # Verificar que el libro existe
        libro_existente = libro_crud.obtener_libro(libro_id)
        if not libro_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado"
            )

        # Filtrar campos que no son None
        campos_actualizacion = {
            k: v for k, v in libro_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return libro_existente

        libro_actualizado = libro_crud.actualizar_libro(
            libro_id, **campos_actualizacion
        )
        return libro_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar libro: {str(e)}",
        )


@router.delete("/{libro_id}", response_model=RespuestaAPI)
async def eliminar_libro(libro_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un libro."""
    try:
        libro_crud = LibroCRUD(db)

        # Verificar que el libro existe
        libro_existente = libro_crud.obtener_libro(libro_id)
        if not libro_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado"
            )

        eliminado = libro_crud.eliminar_libro(libro_id)
        if eliminado:
            return RespuestaAPI(mensaje="Libro eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar libro",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar libro: {str(e)}",
        )
