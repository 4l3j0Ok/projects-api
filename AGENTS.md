# AGENTS.md - Coding Guidelines for Agentic Developers

This document contains essential information for agentic coding agents operating in this repository.

## Project Overview

**projects-api** is a FastAPI-based REST API for managing projects with image handling capabilities. Built with FastAPI, SQLModel, and SQLAlchemy on Python 3.14+.

## Build & Test Commands

### Development Setup
```bash
# Install dependencies
uv sync

# Run development server with auto-reload
cd src && python main.py
```

### Running Tests
```bash
# No pytest configured yet - tests should be added to tests/ directory
pytest tests/
# Run single test
pytest tests/test_file.py::test_function_name -v
```

### Linting & Formatting
```bash
# No linting tools configured - should add ruff or similar
# Format: ruff format .
# Lint: ruff check . --fix
```

### Build & Deployment
```bash
# Docker build (multiplatform: amd64, arm64)
docker build -t alejoide/projects-api:latest .
# CI/CD via Woodpecker tags trigger deployment
```

## Code Style Guidelines

### Imports
- **Order**: Standard library → Third-party → Local (separated by blank lines)
- **Style**: Use relative imports for local modules (e.g., `from core.config import AppConfig`)
- **Format**: Import specific items, avoid wildcard imports
- **Grouped**: When multiple imports from same module, separate on same line (e.g., `from fastapi import APIRouter, Depends, File`)

### Formatting & Structure
- **Indentation**: 4 spaces (Python standard)
- **Line length**: No strict limit observed, but keep reasonable
- **Classes**: Use dataclass for config, regular classes for services
- **Functions**: Use snake_case for functions, PascalCase for classes
- **Constants**: UPPER_CASE for configuration values

### Type Hints
- **Required**: Use type hints on all function signatures and return types
- **Optional fields**: Use `Optional[Type]` from typing module
- **SQLModel fields**: Include `Field()` with descriptive metadata
- **Generic types**: Use `list[Type]` (Python 3.9+) or `List[Type]`

### Naming Conventions
- **Functions**: snake_case (e.g., `create_project()`, `_ensure_images_directory()`)
- **Classes**: PascalCase (e.g., `ProjectService`, `ProjectBase`)
- **Private/Internal**: Prefix with underscore (e.g., `_save_image_to_file()`)
- **Constants**: UPPER_CASE (e.g., `IMAGES_DIR`, `LOG_NAME`)
- **Database tables**: lowercase with underscores (e.g., `__tablename__ = "projects"`)

### Error Handling
- **HTTP Errors**: Use `HTTPException` from FastAPI for API responses with status codes
- **Error Detail**: Include descriptive Spanish or English messages
- **Try/Except**: Catch specific exceptions, not bare except
- **Logging**: Use the custom logger for non-critical errors and info

Example:
```python
try:
    # operation
except SpecificError as e:
    raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
```

### Documentation
- **Docstrings**: Include for complex methods in Spanish or English
- **Comments**: Use Spanish for comments matching codebase language
- **Inline comments**: Minimal; code should be self-documenting

## Project Structure

```
src/
├── main.py              # FastAPI app setup, lifespan, middlewares
├── core/
│   ├── config.py        # Configuration dataclasses
│   ├── database.py      # Database initialization & session management
│   └── logger.py        # Custom colorized logger setup
├── models/              # SQLModel models (Project, ProjectBase, etc.)
├── routers/             # API route handlers
├── services/            # Business logic layer (ProjectService)
├── schemas/             # Pydantic schemas (if needed)
└── data/
    └── images/          # Stored project images (WebP format)
```

## Key Dependencies & Usage

- **FastAPI**: Web framework with async support
- **SQLModel**: SQLAlchemy + Pydantic integration for models
- **Uvicorn**: ASGI server
- **PIL/Pillow**: Image processing (WebP conversion)
- **python-dotenv**: Environment variable loading
- **colorlog**: Colored logging output

## Configuration & Environment

Configuration is managed via dataclasses in `core/config.py`:
- `AppConfig`: API settings (host, port, CORS, etc.)
- `DatabaseConfig`: SQLite/PostgreSQL connection
- `PathConfig`: Directory paths
- `LoggerConfig`: Logging configuration

Environment variables (see `.env.example`):
- `APP_HOST`, `APP_PORT`: Server settings
- `DB_TYPE`: Database type (sqlite/postgresql)
- `DEV_MODE`: Enable hot-reload and docs
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## Key Patterns & Conventions

### Service Layer
Services are static method containers for business logic:
```python
class ProjectService:
    @staticmethod
    def _helper_method(): pass
    
    @staticmethod
    def public_method(): pass
```

### Router Pattern
Routers include prefix and tags for OpenAPI documentation:
```python
router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=list[ProjectRead])
def get_projects(session: Session = Depends(get_session)):
    return ProjectService.get_projects(session)
```

### Model Inheritance
Use SQLModel inheritance for DRY principle:
```python
class ProjectBase(SQLModel): pass
class ProjectInternal(ProjectBase): pass
class Project(ProjectInternal, table=True): pass
class ProjectCreate(ProjectBase): pass
class ProjectRead(ProjectBase): pass
```

### Image Handling
Images are converted to WebP format, stored locally, and served via static mount at `/images` route.

## Testing Standards (To Be Established)

- Test files: `tests/test_*.py` or `*_test.py`
- Framework: pytest (recommended, not yet configured)
- Fixtures: Use conftest.py for shared test utilities
- Mocking: Mock database sessions for unit tests

## Common Tasks

### Add a new endpoint
1. Create model in `models/`
2. Add service methods in `services/`
3. Add route in `routers/`
4. Update OpenAPI docs via `response_model` and `tags`

### Add database migration
1. Update models in `models/`
2. Tables auto-create via `SQLModel.metadata.create_all()`
3. Or use Alembic for production migrations

### Handle errors
- Use `HTTPException(status_code=..., detail="...")` in routes
- Log via `logger.error()` for debugging
- Return meaningful error messages to clients
