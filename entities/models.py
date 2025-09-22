"""
Archivo que importa todos los modelos para evitar dependencias circulares
"""

from audiolibro_categoria import Audiolibro
from comic_categoria import Comic


from libro_categoria import Libro
from mapa_categoria import Mapa
from periodico_categoria import Periodico
from Prestamo import Prestamo
from producto import Producto
from revista_categoria import Revista
from tesis_categoria import Tesis


from usuario import Usuario


__all__ = [
    "Usuario",
    "Producto",
    "Prestamo",
    "Libro",
    "Revista",
    "Periodico",
    "Audiolibro",
    "Comic",
    "Mapa",
    "Tesis",
]
