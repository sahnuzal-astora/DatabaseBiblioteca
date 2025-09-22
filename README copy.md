# Sistema de Gestión de Biblioteca Digital

Este proyecto implementa un sistema de gestión de biblioteca digital utilizando Python, SQLAlchemy y PostgreSQL. El sistema permite a los administradores gestionar productos (libros, revistas, periódicos, etc.), realizar préstamos y devoluciones, y mantener un registro de usuarios y productos.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

├── database/
│ └── config.py # Configuración de conexión y sesión de base de datos
│
├── entities/ # Modelos de base de datos (ORM con SQLAlchemy)
│ ├── usuario.py # Modelo Usuario
│ ├── producto.py # Modelo Producto
│ ├── prestamo.py # Modelo Prestamo
│ ├── libro_categoria.py # Categoría: Libro
│ ├── revista_categoria.py # Categoría: Revista
│ ├── periodico_categoria.py # Categoría: Periódico
│ ├── audiolibro_categoria.py # Categoría: Audiolibro
│ ├── comic_categoria.py # Categoría: Cómic
│ ├── mapa_categoria.py # Categoría: Mapa
│ ├── tesis_categoria.py # Categoría: Tesis
│ └── init.py # Centraliza imports de modelos
│
├── crud/ # Operaciones CRUD para cada entidad
│ ├── usuario_crud.py
│ ├── producto_crud.py
│ ├── prestamo_crud.py
│ └── ...
│
├── menu.py # Menú principal de interacción en consola
├── main.py # Punto de entrada del sistema
└── README.md # Documentación del proyecto

## Funcionalidades Principales

1. **Login**: 
   - El administrador puede iniciar sesión con su correo y contraseña.
   - Si no existe un administrador por defecto, el sistema crea uno automáticamente (`admin@system.com` / `admin123`).

2. **Gestión de Productos**:
   - El administrador puede agregar productos con categorías específicas (libros, revistas, cómics, etc.).
   - Cada producto tiene atributos como título, autor, año, y una categoría específica con atributos adicionales.

3. **Mostrar Productos**:
   - Se puede listar todos los productos registrados en la biblioteca, mostrando su estado (disponible o prestado).

4. **Préstamos y Devoluciones**:
   - Los productos pueden ser prestados a usuarios registrados.
   - Los productos prestados pueden ser devueltos, actualizando su estado a disponible.

5. **Ciclo del Sistema**:
   - Al salir del sistema, el usuario vuelve al menú de login.

## Requisitos

- Python 3.8 o superior
- PostgreSQL
- Las dependencias del proyecto están listadas en `requirements.txt`.

## Instalación y Ejecución

Sigue estos pasos para instalar y ejecutar el sistema:

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd tarea_migrar

2. **crear un entorno virtual**:
   python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **instalar dependencias**:
pip install -r requirements.txt

4. **configurar la base de datos**:
    Crea una base de datos en PostgreSQL.
    Configura las credenciales en un archivo .env:
    DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_bd

5. **ejecutar migraciones**:
    alembic upgrade head

6. **ejecutar el sistema**:
    python [menu.py](http://_vscodecontentref_/28)

👥 Usuarios

Administrador (local):

Email: admin@gmail.com

Clave: 123

Permisos: puede gestionar productos, categorías y usuarios.

Usuarios normales:

Se registran en el sistema.

Pueden realizar préstamos y devoluciones.

🔒 El sistema limita a 3 intentos de login. Si se superan, el proceso termina.

📦 Productos y Categorías

Un producto es la entidad principal, y siempre pertenece a una categoría.
Cada categoría agrega atributos específicos:

Libro → género, páginas

Revista → edición

Periódico → fecha publicación

Audiolibro → narrador, duración, formato

Cómic → ilustrador, editorial, volumen

Mapa → región, escala, tipo

Tesis → universidad, director, grado académico

Campo clave:

disponible = True/False → indica si el producto está en préstamo o no.

🔄 Préstamos

Relacionan un usuario con un producto.

Al prestar:

El producto pasa a disponible = False.

Se guarda la fecha_prestamo.

Al devolver:

El producto vuelve a disponible = True.

Se registra fecha_devolucion.

Se actualiza el estado devuelto = True.

1. Iniciar Sesión
Al ejecutar el sistema, se mostrará un menú de inicio de sesión. Si no existe un administrador por defecto, el sistema lo creará automáticamente:

Email: admin@system.com
Contraseña: admin123

=== LOGIN BIBLIOTECA ===
Email: admin@system.com
Clave: admin123
Bienvenido Administrador (local)

2. Crear un Producto
Desde el menú de administrador, selecciona la opción 1 para crear un producto. Ingresa los datos solicitados y selecciona la categoría

--- CREAR PRODUCTO ---
Título: El Principito
Autor: Antoine de Saint-Exupéry
Año: 1943

Seleccione categoría del producto:
1. Libro
2. Revista
3. Periódico
4. Audiolibro
5. Cómic
6. Mapa
7. Tesis
Opción: 1

Género: Ficción
Número de páginas: 96
Libro creado con éxito.

3. Mostrar Productos
Selecciona la opción 2 para listar los productos registrados.

--- LISTADO DE PRODUCTOS ---
[1] El Principito - Antoine de Saint-Exupéry (1943) | Estado: Disponible

4. Prestar un Producto
Selecciona la opción 3 para prestar un producto. Ingresa el ID del producto.

Ingrese ID del producto (UUID): 1
Producto prestado correctamente

5. Devolver un Producto
Selecciona la opción 4 para devolver un producto. Ingresa el ID del producto.

Ingrese ID del producto a devolver (UUID): 1
Producto devuelto correctamente

6. Cerrar Sesión
Selecciona la opción 0 para cerrar sesión y volver al menú de inicio de sesión.

Cerrando sesión...

Notas
Administrador por defecto: Si no existe un administrador, el sistema crea uno automáticamente.


Base de datos: El sistema utiliza SQLAlchemy como ORM y Alembic para migraciones.