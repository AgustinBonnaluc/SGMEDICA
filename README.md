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

Requisitos: Docker Desktop, Python 3.11 y Node 22.

### Instalación (una sola vez)

```bash
cp .env.example .env
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt -r simulador_iot/requirements.txt
python -m venv alertas/.venv
alertas/.venv/Scripts/python -m pip install -r alertas/requirements.txt
npm --prefix frontend install
```

### Ejecución

Cada comando va en una terminal distinta, desde la raíz del repositorio.

```bash
docker compose up -d
cd backend && .venv/Scripts/python -m uvicorn app.main:app --reload
cd alertas && .venv/Scripts/python -m uvicorn app.main:app --port 8001
npm --prefix frontend run dev
backend/.venv/Scripts/python simulador_iot/simulador.py <paciente_id>
```

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
