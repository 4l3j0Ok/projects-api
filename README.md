# Projects API

API simple para gestionar los proyectos que se visualizan en [www.alejoide.com](https://www.alejoide.com)

## Estructura del proyecto

El proyecto se estructura en los siguientes archivos y carpetas:

```sh
.
├── AGENTS.md # Guía operativa para agentes (comandos, estilo y convenciones del repo)
├── CHANGELOG.md # Historial de cambios funcionales y técnicos entre versiones
├── Dockerfile # Imagen de la API lista para despliegue en contenedores
├── pyproject.toml # Dependencias, metadata del proyecto y configuración de tooling Python
├── README.md # Documentación de uso, estructura y puesta en marcha del servicio
├── src # Código fuente de la API
│   ├── core # Infraestructura compartida (configuración, DB y logging)
│   │   ├── config.py # Variables de entorno y parámetros globales de ejecución
│   │   ├── database.py # Inicialización/conexión de la base de datos y utilidades asociadas
│   │   └── logger.py # Configuración centralizada de logs para observabilidad
│   ├── main.py # Punto de entrada: crea la app, registra routers y middlewares
│   ├── models # Modelos de datos usados por la API
│   │   └── project.py # Esquemas/entidad de proyecto para validación y transporte
│   ├── routers # Definición de endpoints HTTP y manejo de requests/responses
│   │   └── projects.py # Rutas de proyectos (listado, alta, edición, baja, etc.)
│   └── services # Lógica de negocio desacoplada de la capa HTTP
│       └── projects.py # Operaciones de proyectos (consultas, reglas y persistencia)
└── uv.lock # Versiones exactas de dependencias para builds reproducibles
```

## Iniciar el proyecto

Se utiliza la herramienta [uv](https://astral.sh/uv/) para gestionar el entorno virtual y las dependencias. Para iniciar el proyecto, sigue estos pasos:
1. Clona el repositorio:

```sh
git clone https://github.com/4l3j0Ok/projects-api.git
cd projects-api
```
2. Instala las dependencias:

```sh
uv sync
```
3. Inicia el servidor de desarrollo:
```sh
uv run src/main.py
```
El servidor estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva de la API en `http://localhost:8000/docs`.

## Contribuir al proyecto

El proyecto está enfocado exclusivamente para la gestión de proyectos de [www.alejoide.com](https://www.alejoide.com), el cual es un portafolio personal. Se aceptan contribuciones que mejoren la funcionalidad, seguridad o rendimiento de la API, siempre y cuando estén alineadas con el propósito específico de gestionar los proyectos del portafolio.

Podes forkear el repositorio, realizar tus cambios y luego abrir un pull request para revisión. Asegúrate de seguir las convenciones de código y de incluir pruebas unitarias para cualquier nueva funcionalidad o corrección de bugs.

## Licencia

