"""
Módulo de endpoints para la gestión de productos.

Proporciona las rutas y operaciones CRUD (crear, leer, actualizar y eliminar)
para manejar los productos en el sistema. Cada endpoint está protegido con manejo
de errores y devuelve respuestas tipadas según los esquemas definidos en `schemas`.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.config import get_db
from crud.producto_crud import ProductoCRUD
from schemas import ProductoCreate, ProductoUpdate, ProductoResponse, RespuestaAPI

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[ProductoResponse])
async def obtener_productos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los productos con soporte de paginación.

    Args:
        skip (int, optional): Número de registros a omitir. Por defecto es 0.
        limit (int, optional): Máximo número de productos a devolver. Por defecto es 100.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[ProductoResponse]: Lista de productos registrados en la base de datos.

    Raises:
        HTTPException:
            - 500: Si ocurre un error al consultar los productos.
    """
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
    """
    Obtener un producto específico por su ID.

    Args:
        producto_id (UUID): Identificador único del producto.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ProductoResponse: Objeto con la información del producto solicitado.

    Raises:
        HTTPException:
            - 404: Si el producto no existe.
            - 500: Si ocurre un error en la consulta a la base de datos.
    """
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
    """
    Buscar productos por título con coincidencia parcial.

    Args:
        titulo (str): Título o parte del título a buscar.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[ProductoResponse]: Lista de productos que coinciden con el criterio de búsqueda.

    Raises:
        HTTPException:
            - 500: Si ocurre un error al realizar la búsqueda.
    """
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
    """
    Crear un nuevo producto en la base de datos.

    Args:
        producto (ProductoCreate): Datos necesarios para crear el producto.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ProductoResponse: Objeto con la información del producto creado.

    Raises:
        HTTPException:
            - 400: Si los datos proporcionados no son válidos.
            - 500: Si ocurre un error al crear el producto.
    """
    try:
        producto_crud = ProductoCRUD(db)
        return producto_crud.crear_producto(
            titulo=producto.titulo,
            autor=producto.autor,
            anio=producto.anio,
            id_usuario_crea=producto.id_usuario_crea,
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
    """
    Actualizar los datos de un producto existente.

    Args:
        producto_id (UUID): Identificador único del producto.
        producto_data (ProductoUpdate): Campos opcionales a modificar.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ProductoResponse: Objeto con los datos actualizados del producto.

    Raises:
        HTTPException:
            - 404: Si el producto no existe.
            - 400: Si los datos proporcionados no son válidos.
            - 500: Si ocurre un error durante la actualización.
    """
    try:
        producto_crud = ProductoCRUD(db)
        producto_existente = producto_crud.obtener_producto(producto_id)

        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        campos_actualizacion = {
            k: v for k, v in producto_data.dict().items() if v is not None
        }

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
    """
    Eliminar un producto existente de la base de datos.

    Args:
        producto_id (UUID): Identificador único del producto a eliminar.
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        RespuestaAPI: Mensaje de confirmación con el resultado de la operación.

    Raises:
        HTTPException:
            - 404: Si el producto no existe.
            - 500: Si ocurre un error al intentar eliminar el producto.
    """
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
