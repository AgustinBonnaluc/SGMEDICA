# SGMEDICA

Sistema de gestión médica y telemedicina. Proyecto de la materia Técnicas Avanzadas de Programación.

## Estructura

| Carpeta | Contenido |
|---|---|
| `backend/` | API principal con FastAPI: REST y GraphQL |
| `alertas/` | Microservicio de alertas |
| `simulador_iot/` | Simulador de dispositivo IoT |
| `frontend/` | Interfaz con React y Vite |

## Cómo ejecutar

### Con Docker

Requisito: Docker Desktop.

```bash
cp .env.example .env
docker compose up -d --build
```

Levanta las tres bases, el backend, el microservicio de alertas y el frontend. Se apaga con `docker compose down`.

El detalle del despliegue está en [DESPLIEGUE_DOCKER.md](DESPLIEGUE_DOCKER.md).

El simulador se ejecuta aparte, porque recibe el id del paciente:

```bash
backend/.venv/Scripts/python simulador_iot/simulador.py <paciente_id>
```

### Sin Docker para los servicios

Requisitos: Docker Desktop, Python 3.11 y Node 22. Solo las bases corren en contenedores.

#### Instalación (una sola vez)

```bash
cp .env.example .env
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt -r simulador_iot/requirements.txt
python -m venv alertas/.venv
alertas/.venv/Scripts/python -m pip install -r alertas/requirements.txt
npm --prefix frontend install
```

#### Ejecución

Cada comando va en una terminal distinta, desde la raíz del repositorio.

```bash
docker compose up -d postgres mongo redis
cd backend && .venv/Scripts/python -m uvicorn app.main:app --reload
cd alertas && .venv/Scripts/python -m uvicorn app.main:app --port 8001
npm --prefix frontend run dev
backend/.venv/Scripts/python simulador_iot/simulador.py <paciente_id>
```

### Direcciones

| Servicio | Dirección |
|---|---|
| Frontend | http://localhost:5173 |
| API REST (documentación) | http://localhost:8000/docs |
| API GraphQL | http://localhost:8000/graphql |
| Alertas (WebSocket) | ws://localhost:8001/ws/alertas |

### Tests

```bash
cd backend && .venv/Scripts/python -m pytest
cd alertas && .venv/Scripts/python -m pytest
```
