"""
Sistema de gestión de biblioteca digital con ORM y Neon PostgreSQL
Incluye login para administrador
"""

from types import SimpleNamespace
import sys
from typing import Optional
from types import SimpleNamespace
from crud.producto_crud import ProductoCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.prestamo_crud import PrestamoCRUD
from crud.libro_crud import LibroCRUD
from crud.revista_crud import RevistaCRUD
from crud.periodico_crud import PeriodicoCRUD
from crud.audiolibro_crud import AudiolibroCRUD
from crud.comic_crud import ComicCRUD
from crud.mapa_crud import MapaCRUD
from crud.tesis_crud import TesisCRUD

from database.config import SessionLocal, create_tables
from entities.usuario import (
    Usuario,
)
import getpass


class SistemaBiblioteca:
    def __init__(self):
        self.db = SessionLocal()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.producto_crud = ProductoCRUD(self.db)
        self.prestamo_crud = PrestamoCRUD(self.db)
        self.libro_crud = LibroCRUD(self.db)
        self.revista_crud = RevistaCRUD(self.db)
        self.periodico_crud = PeriodicoCRUD(self.db)
        self.audiolibro_crud = AudiolibroCRUD(self.db)
        self.comic_crud = ComicCRUD(self.db)
        self.mapa_crud = MapaCRUD(self.db)
        self.tesis_crud = TesisCRUD(self.db)

        self.usuario_actual: Optional[object] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def login(self) -> bool:
        print("\n=== LOGIN BIBLIOTECA ===")
        intentos = 0
        max_intentos = 3

        while intentos < max_intentos:
            email = input("Email: ").strip()
            clave = input("Clave: ").strip()

            if email == "admin@gmail.com" and clave == "123":
                self.usuario_actual = SimpleNamespace(
                    email=email,
                    nombre="Admin",
                    telefono="N/A",
                    es_admin=True,
                    id_usuario=None,
                )
                print(" Bienvenido Administrador (local)")
                return True

            usuario = self.usuario_crud.autenticar_usuario(email, clave)
            if usuario:
                self.usuario_actual = usuario
                self.usuario_actual.es_admin = bool(getattr(usuario, "es_admin", False))
                print(f" Bienvenido {usuario.nombre}")
                return True

            intentos += 1
            print(f" Credenciales incorrectas. Intento {intentos} de {max_intentos}\n")

        print(" Se superó el número máximo de intentos. Cerrando sistema...")
        sys.exit(1)

    def mostrar_menu(self):

        while True:
            if getattr(self.usuario_actual, "es_admin", False):
                salir = self.menu_admin()
            else:
                salir = self.menu_usuario()

            if salir:
                self.usuario_actual = None
                break

    def menu_admin(self):
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Crear producto")
        print("2. Mostrar productos")
        print("3. Prestar producto")
        print("4. Devolver producto")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            self.crear_producto()
        elif opcion == "2":
            self.mostrar_productos()
        elif opcion == "3":
            self.prestar_producto()
        elif opcion == "4":
            self.devolver_producto()
        elif opcion == "0":
            print(" Cerrando sesión...")
            return True
        else:
            print(" Opción inválida")
        return False

    def menu_usuario(self):
        print("\n=== MENÚ USUARIO ===")
        print("1. Mostrar materiales")
        print("2. Devolver material")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            self.mostrar_productos()
        elif opcion == "2":
            self.devolver_producto()
        elif opcion == "0":
            print(" Cerrando sesión...")
            return True
        else:
            print(" Opción inválida")
        return False

    def crear_producto(self):

        print("\n--- CREAR PRODUCTO ---")
        titulo = input("Título: ").strip()
        if not titulo:
            print(" Título requerido.")
            return

        autor = input("Autor: ").strip()
        if not autor:
            print(" Autor requerido.")
            return

        while True:
            anio_str = input("Año: ").strip()
            if not anio_str.isdigit():
                print(" Debe ingresar un número entero para el año.")
                continue
            anio = int(anio_str)
            break

        print("\nSeleccione categoría del producto:")
        print("1. Libro")
        print("2. Revista")
        print("3. Periódico")
        print("4. Audiolibro")
        print("5. Cómic")
        print("6. Mapa")
        print("7. Tesis")

        opcion = input("Opción: ").strip()
        if not opcion.isdigit():
            print(" Opción inválida (debe ser número).")
            return

        opcion = int(opcion)

        id_usuario_crea = getattr(self.usuario_actual, "id_usuario", None)
        if id_usuario_crea is None:

            admin_db = self.usuario_crud.obtener_admin_por_defecto()
            if admin_db:
                id_usuario_crea = getattr(admin_db, "id_usuario", None)
            else:
                print(" No se encontró un usuario administrador en la base de datos.")
                print(
                    "   Cree primero un admin en la BD o inicie sesión con un usuario real."
                )
                return

        try:
            nuevo_producto = self.producto_crud.crear_producto(
                titulo=titulo, autor=autor, anio=anio, id_usuario_crea=id_usuario_crea
            )
        except ValueError as e:
            print(f" Error al crear producto: {e}")
            return
        except Exception as e:
            print(f" Error inesperado al crear producto: {e}")
            return

        if not nuevo_producto:
            print(" Error al crear el producto base.")
            return

        producto_id = getattr(nuevo_producto, "id_producto", None) or getattr(
            nuevo_producto, "id", None
        )
        if producto_id is None:
            print(" No se obtuvo el id del producto creado. Verifica ProductoCRUD.")
            return

        try:
            if opcion == 1:

                genero = input("Género: ").strip()
                paginas_str = input("Número de páginas: ").strip()
                if not paginas_str.isdigit():
                    print(" Páginas debe ser un número entero.")
                    return
                paginas = int(paginas_str)
                self.libro_crud.crear_libro(
                    genero=genero, paginas=paginas, producto_id=producto_id
                )
                print(" Libro creado con éxito.")
            elif opcion == 2:
                edicion = input("Edición: ").strip()
                self.revista_crud.crear_revista(
                    edicion=edicion, producto_id=producto_id
                )
                print(" Revista creada con éxito.")
            elif opcion == 3:
                fecha_publicacion = input("Fecha de publicación: ").strip()
                self.periodico_crud.crear_periodico(
                    fecha_publicacion=fecha_publicacion, producto_id=producto_id
                )
                print(" Periódico creado con éxito.")
            elif opcion == 4:
                narrador = input("Narrador: ").strip()
                duracion_str = input("Duración (minutos): ").strip()
                if not duracion_str.isdigit():
                    print(" Duración debe ser un número entero (minutos).")
                    return
                duracion = int(duracion_str)
                formato = input("Formato (mp3, wav, etc.): ").strip()
                self.audiolibro_crud.crear_audiolibro(
                    narrador=narrador,
                    duracion=duracion,
                    formato=formato,
                    producto_id=producto_id,
                )
                print(" Audiolibro creado con éxito.")
            elif opcion == 5:
                ilustrador = input("Ilustrador: ").strip()
                editorial = input("Editorial: ").strip()
                volumen = input("Volumen: ").strip()
                self.comic_crud.crear_comic(
                    ilustrador=ilustrador,
                    editorial=editorial,
                    volumen=volumen,
                    producto_id=producto_id,
                )
                print(" Cómic creado con éxito.")
            elif opcion == 6:
                region = input("Región: ").strip()
                escala = input("Escala: ").strip()
                tipo = input("Tipo de mapa: ").strip()
                self.mapa_crud.crear_mapa(
                    region=region, escala=escala, tipo=tipo, producto_id=producto_id
                )
                print(" Mapa creado con éxito.")
            elif opcion == 7:
                universidad = input("Universidad: ").strip()
                director = input("Director: ").strip()
                grado = input("Grado Académico: ").strip()
                self.tesis_crud.crear_tesis(
                    universidad=universidad,
                    director=director,
                    grado_academico=grado,
                    producto_id=producto_id,
                )
                print(" Tesis creada con éxito.")
            else:
                print(
                    " Opción inválida. Producto base ya creado (puede eliminarlo manualmente si no desea conservarlo)."
                )
        except Exception as e:
            print(f" Error creando la categoría: {e}")

    def mostrar_productos(self):
        productos = self.producto_crud.obtener_productos()
        if not productos:
            print(" No hay productos registrados")
            return

        print("\n--- LISTADO DE PRODUCTOS ---")
        for p in productos:

            pid = getattr(p, "id_producto", None) or getattr(p, "id", None)
            estado = "Disponible" if getattr(p, "disponible", True) else "Prestado"
            titulo = getattr(p, "titulo", getattr(p, "name", "Sin título"))
            autor = getattr(p, "autor", "Desconocido")
            anio = getattr(p, "anio", "N/A")
            print(f"[{pid}] {titulo} - {autor} ({anio}) | Estado: {estado}")

    def prestar_producto(self):
        """
        Ahora acepta ID tal cual (UUID string) — no se fuerza a int.
        Solo usuarios reales (con id_usuario) pueden prestar; admin local no.
        """
        id_producto = input("Ingrese ID del producto (UUID): ").strip()
        if not id_producto:
            print(" Debe ingresar el ID del producto.")
            return

        user_id = getattr(self.usuario_actual, "id_usuario", None)
        if user_id is None:
            print(
                " Admin local no puede pedir préstamos. Inicie sesión con un usuario válido."
            )
            return

        try:
            prestamo = self.prestamo_crud.crear_prestamo(user_id, id_producto)
            if prestamo:
                print(" Producto prestado correctamente")
            else:
                print(" No se pudo realizar el préstamo")
        except Exception as e:
            print(f" Error al prestar: {e}")

    def devolver_producto(self):
        """
        Acepta ID tal cual (UUID string) — no se fuerza a int.
        """
        id_producto = input("Ingrese ID del producto a devolver (UUID): ").strip()
        if not id_producto:
            print(" Debe ingresar el ID del producto.")
            return

        user_id = getattr(self.usuario_actual, "id_usuario", None)
        if user_id is None:
            print(
                " Admin local no puede devolver préstamos por usuario. Inicie sesión con un usuario válido."
            )
            return

        try:
            ok = self.prestamo_crud.devolver_prestamo(user_id, id_producto)
            if ok:
                print(" Producto devuelto correctamente")
            else:
                print(" No se pudo devolver el producto")
        except Exception as e:
            print(f" Error al devolver: {e}")


def main():
    create_tables()
    with SistemaBiblioteca() as sistema:

        admin = sistema.usuario_crud.obtener_admin_por_defecto()
        if not admin:
            from auth.security import PasswordManager

            contrasena_hash = PasswordManager.hash_password("admin123")
            sistema.usuario_crud.crear_usuario(
                nombre="Administrador del sistema",
                email="admin@system.com",
                contrasena_hash=contrasena_hash,
                es_admin=True,
            )
            print(" Usuario administrador creado: admin@system.com / admin123")
        else:
            print(f" Admin existente en BD: {admin.email}")

        while True:
            if sistema.login():
                sistema.mostrar_menu()


if __name__ == "__main__":
    main()
