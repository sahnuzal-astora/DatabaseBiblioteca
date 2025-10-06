from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.config import get_db
from crud.producto_crud import ProductoCRUD
from schemas import ProductoCreate, ProductoUpdate, ProductoResponse, RespuestaAPI

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
async def obtener_productos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los productos con paginación."""
    try:
        producto_crud = ProductoCRUD(db)
        return producto_crud.obtener_productos(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}",
        )


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Obtener un producto por ID."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.obtener_producto(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener producto: {str(e)}",
        )


@router.get("/buscar/", response_model=List[ProductoResponse])
async def buscar_por_titulo(titulo: str, db: Session = Depends(get_db)):
    """Buscar productos por título (búsqueda parcial)."""
    try:
        producto_crud = ProductoCRUD(db)
        return producto_crud.buscar_productos_por_titulo(titulo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar productos: {str(e)}",
        )


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto."""
    try:
        producto_crud = ProductoCRUD(db)
        return producto_crud.crear_producto(
            titulo=producto.titulo,
            autor=producto.autor,
            anio=producto.anio,
            id_usuario_crea=producto.id_usuario_crea,
            id_usuario_edita=producto.id_usuario_edita,
            disponible=producto.disponible,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}",
        )


@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: UUID, producto_data: ProductoUpdate, db: Session = Depends(get_db)
):
    try:
        producto_crud = ProductoCRUD(db)
        producto_existente = producto_crud.obtener_producto(producto_id)

        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        # Campos a actualizar
        campos_actualizacion = {
            k: v for k, v in producto_data.dict().items() if v is not None
        }

        # Sacar id_usuario_edita para evitar duplicado
        id_usuario_edita = campos_actualizacion.pop("id_usuario_edita", None)

        if not campos_actualizacion and not id_usuario_edita:
            return producto_existente

        return producto_crud.actualizar_producto(
            producto_id, id_usuario_edita=id_usuario_edita, **campos_actualizacion
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}",
        )


@router.delete("/{producto_id}", response_model=RespuestaAPI)
async def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un producto."""
    try:
        producto_crud = ProductoCRUD(db)
        producto_existente = producto_crud.obtener_producto(producto_id)

        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        eliminado = producto_crud.eliminar_producto(producto_id)
        if eliminado:
            return RespuestaAPI(mensaje="Producto eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar producto",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}",
        )
