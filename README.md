# Aplicativo Web para la Venta y Cobro Puerta a Puerta

Este proyecto es una aplicación web desarrollada en Python para la gestión integral de ventas y cobros puerta a puerta. Utiliza `pipenv` como entorno virtual y está organizado en módulos para facilitar la administración de las distintas áreas del negocio.

## Estructura del Proyecto

- `api/`: Lógica de la API.
- `clientes/`: Gestión de clientes.
- `cobros/`: Módulo de cobros.
- `empleados/`: Administración de empleados.
- `inventario/`: Control de inventario.
- `inversiones_bonanza/`: Configuración principal del proyecto.
- `pagos/`: Gestión de pagos.
- `productos/`: Administración de productos.
- `proveedores/`: Gestión de proveedores.
- `templates/`: Plantillas HTML.
- `usuarios/`: Gestión de usuarios y autenticación.
- `ventas/`: Módulo de ventas.
- `zonas/`: Administración de zonas.
- `manage.py`: Script de gestión del proyecto.
- `Pipfile` y `Pipfile.lock`: Dependencias del entorno virtual.

## Funcionalidades

- Gestión de empleados, clientes, proveedores y usuarios.
- Administración de productos, inventario y zonas.
- Registro y control de ventas, cobros y pagos.
- Localización GPS de ventas y empleados.
- Interfaz web basada en plantillas.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone  https://github.com/OscarMadera1/invesiones-bonanza.VL.git
   cd invesiones-bonanza.VL
   ```
2. Instala las dependencias con pipenv:
   ```bash
   pipenv install
   ```

## Uso

1. Activa el entorno virtual:
   ```bash
   pipenv shell
   ```
2. Ejecuta la aplicación:
   ```bash
   python manage.py runserver
   ```

## Licencia

Este proyecto está bajo la licencia MIT.